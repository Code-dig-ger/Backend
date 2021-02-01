from rest_framework import generics,status,permissions,views,response,mixins
from .models import ListInfo,Solved,List,ListExtraInfo
from problem.models import Problem
from user.models import User,Profile
from .serializers import (
    GetLadderSerializer,
    GetSerializer,
    GetUserlistSerializer,
    EditUserlistSerializer,
    CreateUserlistSerializer,
    ProblemSerializer,
    UserlistAddSerializer,
    UpdateLadderSerializer,
    UpdateListSerializer,
    AddProblemsAdminSerializer
)
from django.db.models import Q
from .permissions import IsOwner
from .solved_update import codeforces,uva,atcoder,codechef,spoj
from .cron import updater,cron_atcoder,cron_codechef,cron_codeforces,cron_spoj,cron_uva,codechef_list
from django.core.paginator import Paginator
from user.permissions import *
from user.exception import *

def getqs(qs,page_size,page):
    qs = qs[page_size*(page-1):page_size*page]
    return qs

class TopicwiseGetListView(generics.ListAPIView):
    serializer_class=GetSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True) & Q(public=True) & Q(owner__is_staff=True))

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user
        return data

class TopicWiseRetrieveView(views.APIView):
    permission_classes = [AuthenticatedOrReadOnly]
    
    def get_object(self,slug):
        if List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True)  & Q(public=True) & Q(owner__is_staff=True) & Q(slug=slug)).exists():
            return List.objects.get(slug=slug)
        raise NotFoundException("The list with the given slug does not exist")

    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page = self.request.GET.get('page',None)
        page_size = 6
        description = curr_list.description
        name= curr_list.name
        difficulty = None
        video_link = None
        contest_link = None
        editorial = None
        if ListExtraInfo.objects.filter(curr_list=curr_list).exists():
            qs = ListExtraInfo.objects.get(curr_list=curr_list)
            difficulty = qs.difficulty
            video_link = qs.video_link
            contest_link = qs.contest_link
            editorial = qs.editorial
        
        problem_qs = curr_list.problem.all().order_by('rating','id')
        total = curr_list.problem.all().count()
        cnt = total//page_size
        if total % page_size != 0:
            cnt += 1
        path = request.build_absolute_uri('/lists/topicwise/list/' + str(slug) + '?')
        user = self.request.user
        if user.is_anonymous:
            user = None
        completed = True
        if not page:
            if cnt == 0 :
                return response.Response({'status' : 'OK' , 'result' : []})
            page = 1
            temp = { 'F' : True, 'A' : True, 'U' : True}
            while page <= cnt:
                qs = getqs(problem_qs,page_size,page)
                for ele in qs:
                    solve = Solved.objects.filter(user=user,problem=ele)
                    if not solve.exists():
                        if ele.platform == 'F' and temp['F']:
                            temp['F'] = False
                            codeforces(user)
                        elif ele.platform == 'A' and temp['A']:
                            temp['A'] = False
                            atcoder(user)
                        elif ele.platform == 'U' and temp['U']:
                            temp['U'] = False
                            uva(user)
                        elif ele.platform == 'S':
                            spoj(user,ele)
                        elif ele.platform == 'C':
                            codechef(user,ele)
                for ele in qs:
                    solve = Solved.objects.filter(user = user,problem=ele)
                    if not solve.exists():
                        completed = False
                        break
                if not completed : 
                    break
                page += 1
            if completed :
                page = 1
            qs = getqs(problem_qs,page_size,page)
            if page == cnt :
                Next = None
            else :
                Next = path + 'page='+str(page+1)
            if page == 1:
                Prev = None
            else :
                Prev = path + 'page='+str(page-1)
            res= {
                'status' : "OK",
                'result' : ProblemSerializer(qs,many=True,context = {"slug" : curr_list,"user" : user}).data,
                'link' : {
                    'first' : path + "page=1",
                    'last' : path + "page=" + str(cnt),
                    'prev' : Prev,
                    'next' : Next,
                },
                'meta' : {
                    'user' : user,
                    'completed' : True,
                    'name' : name,
                    'description' : description,
                    'difficulty' : difficulty,
                    'video_link' : video_link,
                    'contest_link' : contest_link,
                    'editorial' : editorial,
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/topicwise/list/' + str(slug)),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : total
                }
            }
            if user :
                res['meta']['user'] = user.username
            if not completed:
                res['meta']['completed'] = False
            return response.Response(res)
        else:
            if cnt == 0 :
                return response.Response({'status' : 'OK' , 'result' : []})
            if page.isdigit():
                page = int(page)
            else: 
                return response.Response({'status' : 'FAILED' , 'error' : 'Page must be an integer.'},status=status.HTTP_400_BAD_REQUEST)
            if page > cnt : 
                return response.Response({'status' : 'FAILED' , 'error' : 'Page Out of Bound'},status=status.HTTP_400_BAD_REQUEST)
            if page == cnt :
                Next = None
            else :
                Next = path + 'page='+str(page+1)
            if page == 1:
                Prev = None
            else :
                Prev = path + 'page='+str(page-1)
            qs = getqs(problem_qs,page_size,page)
            temp = { 'F' : True, 'A' : True, 'U' : True}
            for ele in qs:
                solve = Solved.objects.filter(user=user,problem=ele)
                if not solve.exists():
                    if ele.platform == 'F' and temp['F']:
                        temp['F'] = False
                        codeforces(user)
                    elif ele.platform == 'A' and temp['A']:
                        temp['A'] = False
                        atcoder(user)
                    elif ele.platform == 'U' and temp['U']:
                        temp['U'] = False
                        uva(user)
                    elif ele.platform == 'S':
                        spoj(user,ele)
                    elif ele.platform == 'C':
                        codechef(user,ele)
            res = {
                'status' : "OK",
                'result' : ProblemSerializer(qs,many=True,context = {"slug" : curr_list,"user" : user}).data,
                'link' : {
                    'first' : path + "page=1",
                    'last' : path + "page=" + str(cnt),
                    'prev' : Prev,
                    'next' : Next,
                },
                'meta' : {
                    'user' : user,
                    'completed' : False,
                    'name' : name,
                    'description' : description,
                    'difficulty' : difficulty,
                    'video_link' : video_link,
                    'contest_link' : contest_link,
                    'editorial' : editorial,
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/topicwise/list/' + str(slug)),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : total
                }
            }
            if user: 
                res['meta']['user'] = user.username
            return response.Response(res)


class TopicwiseGetLadderView(generics.ListAPIView):
    serializer_class=GetLadderSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = True)  & Q(public=True) & Q(owner__is_staff=True))


class TopicWiseLadderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    
    def get_object(self,slug):
        if List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = True)  & Q(public=True) & Q(owner__is_staff=True) & Q(slug=slug)).exists():
            return List.objects.get(slug=slug)
        raise NotFoundException("The list with the given slug does not exist")
    
    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page_size = 6
        name = curr_list.name
        description = curr_list.description
        difficulty = None
        video_link = None
        contest_link = None
        editorial = None
        if ListExtraInfo.objects.filter(curr_list=curr_list).exists():
            qs = ListExtraInfo.objects.get(curr_list=curr_list)
            difficulty = qs.difficulty
            video_link = qs.video_link
            contest_link = qs.contest_link
            editorial = qs.editorial
        
        path = request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '?')
        user = self.request.user
        if user.is_anonymous :
            user = None
        
        problem_qs = curr_list.problem.all()
        if user:
            temp = ['F']
            if Profile.objects.get(owner = user).spoj != None:
                temp.append('S')
            if Profile.objects.get(owner = user).uva_handle != None:
                temp.append('U')
            if Profile.objects.get(owner = user).atcoder != None:
                temp.append('A')
            if Profile.objects.get(owner = user).codechef != None:
                temp.append('C')
            problem_qs = problem_qs.filter(platform__in = temp)
            
        cnt = int(problem_qs.count()/page_size)
        if problem_qs.count() % page_size != 0:
            cnt += 1
        if cnt == 0 :
            return response.Response({'status' : 'OK' , 'result' : []})

        problem_qs = problem_qs.order_by('rating','id')
        page = 1
        curr_prob = None 
        curr_page = None
        completed = False

        
        if user :
            completed = True
            temp = { 'F' : True, 'A' : True, 'U' : True }
            while page <= cnt:
                
                qs = getqs(problem_qs,page_size,page)
                for ele in qs:
                    
                    solve = Solved.objects.filter(user=user,problem=ele)
                    if not solve.exists():
                        if ele.platform == 'F' and temp['F']:
                            temp['F'] = False
                            codeforces(user)
                        elif ele.platform == 'A' and temp['A']:
                            temp['A'] = False
                            atcoder(user)
                        elif ele.platform == 'U' and temp['U']:
                            temp['U'] = False
                            uva(user)
                        elif ele.platform == 'S':
                            spoj(user,ele)
                        elif ele.platform == 'C':
                            codechef(user,ele)
                for ele in qs:
                    solve = Solved.objects.filter(user=user,problem=ele)
                    if not solve.exists():
                        curr_prob = ele.prob_id
                        curr_page = page
                        completed = False
                        break
                if not completed:
                    break
                page += 1

            if completed : 
                page = 1

        if self.request.GET.get('page',None) : 
            page = self.request.GET.get('page',None)
            completed = False
            if page.isdigit():
                page = int(page)
            else: 
                return response.Response({'status' : 'FAILED' , 'error' : 'Page must be an integer.'},status=status.HTTP_400_BAD_REQUEST)
            if page > cnt : 
                return response.Response({'status' : 'FAILED' , 'error' : 'Page Out of Bound'},status=status.HTTP_400_BAD_REQUEST)

        qs = getqs(problem_qs,page_size,page)
        if page == cnt :
            Next = None
        else :
            Next = path + 'page='+str(page+1)
        if page == 1:
            Prev = None
        else :
            Prev = path + 'page='+str(page-1)

        res = {
            'status' : "OK",
            'result' : ProblemSerializer(qs,many=True,context = {"slug" : curr_list,"user" : user}).data,
            'link' : {
                'first' : path + "page=1",
                'last' : path + "page=" + str(cnt),
                'prev' : Prev,
                'next' : Next,
            },
            'meta' : {
                'user' : user,
                'curr_prob' : curr_prob,
                'curr_unsolved_page' : curr_page,
                'completed' : completed,
                'name' : name,
                'description' : description,
                'difficulty' : difficulty,
                'video_link' : video_link,
                'contest_link' : contest_link,
                'editorial' : editorial,
                'current_page' : page,
                'from' : (page-1)*page_size + 1,
                'last_page' : cnt,
                'path' : request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug)),
                'per_page' : page_size,
                'to' : page*page_size,
                'total' : curr_list.problem.all().count()
            }
        }
        if user : 
            res['meta']['user'] = user.username
        return response.Response(res)

class LevelwiseGetListView(generics.ListAPIView):
    serializer_class=GetSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True) & Q(owner__is_staff=True))


class LevelwiseRetrieveView(views.APIView):
    permission_classes = [AuthenticatedOrReadOnly]
    
    def get_object(self,slug):
        if List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True) & Q(owner__is_staff=True) & Q(slug=slug)).exists():
            return List.objects.get(slug=slug)
        raise NotFoundException("The list with the given slug does not exist")

    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page = self.request.GET.get('page',None)
        page_size = 6
        description = curr_list.description
        name= curr_list.name
        difficulty = None
        video_link = None
        contest_link = None
        editorial = None
        if ListExtraInfo.objects.filter(curr_list=curr_list).exists():
            qs = ListExtraInfo.objects.get(curr_list=curr_list)
            difficulty = qs.difficulty
            video_link = qs.video_link
            contest_link = qs.contest_link
            editorial = qs.editorial
        
        problem_qs = curr_list.problem.all().order_by('rating','id')
        total = curr_list.problem.all().count()
        cnt = total//page_size
        if total % page_size != 0:
            cnt += 1
        path = request.build_absolute_uri('/lists/levelwise/list/' + str(slug) + '?')
        user = self.request.user
        if user.is_anonymous:
            user = None
        completed = True
        if not page:
            if cnt == 0 :
                return response.Response({'status' : 'OK' , 'result' : []})
            page = 1
            temp = { 'F' : True, 'A' : True, 'U' : True}
            while page <= cnt:
                qs = getqs(problem_qs,page_size,page)
                for ele in qs:
                    solve = Solved.objects.filter(user=user,problem=ele)
                    if not solve.exists():
                        if ele.platform == 'F' and temp['F']:
                            temp['F'] = False
                            codeforces(user)
                        elif ele.platform == 'A' and temp['A']:
                            temp['A'] = False
                            atcoder(user)
                        elif ele.platform == 'U' and temp['U']:
                            temp['U'] = False
                            uva(user)
                        elif ele.platform == 'S':
                            spoj(user,ele)
                        elif ele.platform == 'C':
                            codechef(user,ele)
                for ele in qs:
                    solve = Solved.objects.filter(user = user,problem=ele)
                    if not solve.exists():
                        completed = False
                        break
                if not completed : 
                    break
                page += 1
            if completed :
                page = 1
            qs = getqs(problem_qs,page_size,page)
            if page == cnt :
                Next = None
            else :
                Next = path + 'page='+str(page+1)
            if page == 1:
                Prev = None
            else :
                Prev = path + 'page='+str(page-1)
            res= {
                'status' : "OK",
                'result' : ProblemSerializer(qs,many=True,context = {"slug" : curr_list,"user" : user}).data,
                'link' : {
                    'first' : path + "page=1",
                    'last' : path + "page=" + str(cnt),
                    'prev' : Prev,
                    'next' : Next,
                },
                'meta' : {
                    'user' : user,
                    'completed' : True,
                    'name' : name,
                    'description' : description,
                    'difficulty' : difficulty,
                    'video_link' : video_link,
                    'contest_link' : contest_link,
                    'editorial' : editorial,
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/levelwise/list/' + str(slug)),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : total
                }
            }
            if user :
                res['meta']['user'] = user.username
            if not completed:
                res['meta']['completed'] = False
            return response.Response(res)
        else:
            if cnt == 0 :
                return response.Response({'status' : 'OK' , 'result' : []})
            if page.isdigit():
                page = int(page)
            else: 
                return response.Response({'status' : 'FAILED' , 'error' : 'Page must be an integer.'},status=status.HTTP_400_BAD_REQUEST)
            if page > cnt : 
                return response.Response({'status' : 'FAILED' , 'error' : 'Page Out of Bound'},status=status.HTTP_400_BAD_REQUEST)
            if page == cnt :
                Next = None
            else :
                Next = path + 'page='+str(page+1)
            if page == 1:
                Prev = None
            else :
                Prev = path + 'page='+str(page-1)
            qs = getqs(problem_qs,page_size,page)
            temp = { 'F' : True, 'A' : True, 'U' : True}
            for ele in qs:
                solve = Solved.objects.filter(user=user,problem=ele)
                if not solve.exists():
                    if ele.platform == 'F' and temp['F']:
                        temp['F'] = False
                        codeforces(user)
                    elif ele.platform == 'A' and temp['A']:
                        temp['A'] = False
                        atcoder(user)
                    elif ele.platform == 'U' and temp['U']:
                        temp['U'] = False
                        uva(user)
                    elif ele.platform == 'S':
                        spoj(user,ele)
                    elif ele.platform == 'C':
                        codechef(user,ele)
            res = {
                'status' : "OK",
                'result' : ProblemSerializer(qs,many=True,context = {"slug" : curr_list,"user" : user}).data,
                'link' : {
                    'first' : path + "page=1",
                    'last' : path + "page=" + str(cnt),
                    'prev' : Prev,
                    'next' : Next,
                },
                'meta' : {
                    'user' : user,
                    'completed' : False,
                    'name' : name,
                    'description' : description,
                    'difficulty' : difficulty,
                    'video_link' : video_link,
                    'contest_link' : contest_link,
                    'editorial' : editorial,
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/topicwise/list/' + str(slug)),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : total
                }
            }
            if user: 
                res['meta']['user'] = user.username
            return response.Response(res)


class LevelwiseGetLadderView(generics.ListAPIView):
    serializer_class=GetLadderSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True) & Q(owner__is_staff=True))


class LevelwiseLadderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    
    def get_object(self,slug):
        if List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True) & Q(owner__is_staff=True) & Q(slug=slug)).exists():
            return List.objects.get(slug=slug)
        raise NotFoundException("The list with the given slug does not exist")
    
    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page_size = 6
        name = curr_list.name
        description = curr_list.description
        difficulty = None
        video_link = None
        contest_link = None
        editorial = None
        if ListExtraInfo.objects.filter(curr_list=curr_list).exists():
            qs = ListExtraInfo.objects.get(curr_list=curr_list)
            difficulty = qs.difficulty
            video_link = qs.video_link
            contest_link = qs.contest_link
            editorial = qs.editorial
        
        path = request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '?')
        user = self.request.user
        if user.is_anonymous :
            user = None
        
        problem_qs = curr_list.problem.all()
        if user:
            temp = ['F']
            if Profile.objects.get(owner = user).spoj != None:
                temp.append('S')
            if Profile.objects.get(owner = user).uva_handle != None:
                temp.append('U')
            if Profile.objects.get(owner = user).atcoder != None:
                temp.append('A')
            if Profile.objects.get(owner = user).codechef != None:
                temp.append('C')
            problem_qs = problem_qs.filter(platform__in = temp)
            
        cnt = int(problem_qs.count()/page_size)
        if problem_qs.count() % page_size != 0:
            cnt += 1
        if cnt == 0 :
            return response.Response({'status' : 'OK' , 'result' : []})

        problem_qs = problem_qs.order_by('rating','id')
        page = 1
        curr_prob = None 
        curr_page = None
        completed = False

        
        if user :
            completed = True
            temp = { 'F' : True, 'A' : True, 'U' : True }
            while page <= cnt:
                
                qs = getqs(problem_qs,page_size,page)
                for ele in qs:
                    
                    solve = Solved.objects.filter(user=user,problem=ele)
                    if not solve.exists():
                        if ele.platform == 'F' and temp['F']:
                            temp['F'] = False
                            codeforces(user)
                        elif ele.platform == 'A' and temp['A']:
                            temp['A'] = False
                            atcoder(user)
                        elif ele.platform == 'U' and temp['U']:
                            temp['U'] = False
                            uva(user)
                        elif ele.platform == 'S':
                            spoj(user,ele)
                        elif ele.platform == 'C':
                            codechef(user,ele)
                for ele in qs:
                    solve = Solved.objects.filter(user=user,problem=ele)
                    if not solve.exists():
                        curr_prob = ele.prob_id
                        curr_page = page
                        completed = False
                        break
                if not completed:
                    break
                page += 1

            if completed : 
                page = 1

        if self.request.GET.get('page',None) : 
            page = self.request.GET.get('page',None)
            completed = False
            if page.isdigit():
                page = int(page)
            else: 
                return response.Response({'status' : 'FAILED' , 'error' : 'Page must be an integer.'},status=status.HTTP_400_BAD_REQUEST)
            if page > cnt : 
                return response.Response({'status' : 'FAILED' , 'error' : 'Page Out of Bound'},status=status.HTTP_400_BAD_REQUEST)

        qs = getqs(problem_qs,page_size,page)
        if page == cnt :
            Next = None
        else :
            Next = path + 'page='+str(page+1)
        if page == 1:
            Prev = None
        else :
            Prev = path + 'page='+str(page-1)

        res = {
            'status' : "OK",
            'result' : ProblemSerializer(qs,many=True,context = {"slug" : curr_list,"user" : user}).data,
            'link' : {
                'first' : path + "page=1",
                'last' : path + "page=" + str(cnt),
                'prev' : Prev,
                'next' : Next,
            },
            'meta' : {
                'user' : user,
                'curr_prob' : curr_prob,
                'curr_unsolved_page' : curr_page,
                'completed' : completed,
                'name' : name,
                'description' : description,
                'difficulty' : difficulty,
                'video_link' : video_link,
                'contest_link' : contest_link,
                'editorial' : editorial,
                'current_page' : page,
                'from' : (page-1)*page_size + 1,
                'last_page' : cnt,
                'path' : request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug)),
                'per_page' : page_size,
                'to' : page*page_size,
                'total' : curr_list.problem.all().count()
            }
        }
        if user : 
            res['meta']['user'] = user.username
        return response.Response(res)


# class updateLadderview(generics.GenericAPIView):
#     serializer_class = UpdateLadderSerializer

#     def post(self,request,*args, **kwargs):
#         prob_id = self.request.GET.get('prob_id')
#         if prob_id == None:
#             codeforces(self.request.user.username)
#             uva(self.request.user.username)
#             atcoder(self.request.user.username)
#         else:
#             if Problem.objects.filter(prob_id=prob_id,platform='F').exists():
#                 codeforces(self.request.user.username)
#             if Problem.objects.filter(prob_id=prob_id,platform='U').exists():
#                 uva(self.request.user.username)
#             if Problem.objects.filter(prob_id=prob_id,platform='A').exists():
#                 atcoder(self.request.user.username)
#             if Problem.objects.filter(prob_id=prob_id,platform='C').exists():
#                 codechef(self.request.user.username,prob_id)
#             if Problem.objects.filter(prob_id=prob_id,platform='S').exists():
#                 spoj(self.request.user.username,prob_id)
#         return response.Response({'status' : "OK",'result' : 'ladder updated'},status = status.HTTP_200_OK)

# class updateListView(generics.GenericAPIView):
#     serializer_class = UpdateListSerializer

#     def post(self,request,*args,**kwargs):
#         list_slug = self.request.GET.get('slug')
#         page = self.request.GET.get('page')
#         if list_slug is None or list_slug == "" :
#             return response.Response(data={'status' : 'FAILED','error' : 'No list provided'})
#         curr_list = List.objects.get(slug=list_slug)
#         cnt = int(curr_list.problem.all().count()/page_size)
#         if curr_list.problem.all().count() % page_size != 0:
#             cnt += 1
#         if page is None or page == "":
#             return response.Response(data={'status' : 'FAILED','error' :'No page provided'})
#         if page > cnt:
#             return response.Response(data={'status' : 'FAILED','error' :'Page out of bounds'})
#         #set page size here and in the serializer list waala
#         page_size = 6
#         problem_qs = curr_list.problem.all().order_by('rating')
#         paginator = Paginator(problem_qs,page_size)

#         qs = paginator.page(page)  
#         check = {'S' : set(),'U' : 0,'C' : set(),'F' : 0,'A' : 0}
#         for prob in qs:
#             platform = prob.platform
#             if not Solved.objects.filter(user=self.request.user,problem__prob_id=prob.prob_id).exists():
#                 if platform == 'S' or platform == 'C':
#                     check[platform].add(prob.prob_id)
#                 else:
#                     check[platform] += 1
#         print(check)
#         if check['F'] > 0:
#             cron_codeforces(self.request.user.username) 
#         if check['U'] > 0:
#             cron_uva(self.request.user.username)
#         if check['A'] > 0:
#             cron_atcoder(self.request.user.username)
#         if len(check['S']) > 0:
#             for item in check['S']:
#                 spoj(self.request.user.username,item)
#         if len(check['C']) > 0:
#             list1 = codechef_list(self.request.user.username)
#             list2 = check['C']
#             final = set((list1) & (list2))
#             for ele in final:
#                 prob = Problem.objects.get(prob_id=ele,platform='C')
#                 user = self.request.user
#                 Solved.objects.create(user=user,problem=prob)
#         return response.Response(data={'status' : 'OK','result' :'list updated'})


class UserlistGetView(generics.ListAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = GetUserlistSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            qs = List.objects.filter(Q(owner=self.request.user) | Q(isAdmin = True))
            return qs
        else:
            qs = List.objects.filter(owner=self.request.user)
            return qs
    

class UserlistCreateView(generics.CreateAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = CreateUserlistSerializer

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)


class UserlistAddProblemView(generics.CreateAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = UserlistAddSerializer

    def post(self,request,*args, **kwargs):
        data = request.data
        prob_id = data.get('prob_id',None)
        slug = data.get('slug',None)
        platform = data.get('platform',None)
        if prob_id is None or slug is None or platform is None:
            return response.Response({"status" : 'FAILED','error' :"prob_id or slug or platform not provided"},status=status.HTTP_400_BAD_REQUEST)
        if not List.objects.filter(slug = slug).exists():
            return response.Response({"status" : 'FAILED','error' :"List with the provided slug does not exist"},status=status.HTTP_400_BAD_REQUEST)
        if not Problem.objects.filter(prob_id = prob_id, platform=platform).exists():
            return response.Response({"status" : 'FAILED','error' :"Problem with the given prob_id and platform does not exist"},status=status.HTTP_400_BAD_REQUEST)
        curr_list = List.objects.get(slug=slug)
        curr_prob = Problem.objects.get(prob_id=prob_id,platform=platform)
        if curr_list.problem.filter(prob_id=prob_id,platform=platform).exists():
            return response.Response({"status" : 'FAILED','error' :"Problem with the given prob_id and platform already exists within the list"},status=status.HTTP_400_BAD_REQUEST)
        curr_list.problem.add(curr_prob)
        return response.Response({"status" : 'OK','result' :"Given problem has been added to the list"},status = status.HTTP_200_OK)


class EditUserlistView(generics.GenericAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = EditUserlistSerializer

    def get_object(self,slug):
        if self.request.user.is_staff:
            if List.objects.filter((Q(isAdmin = True) | Q(owner = self.request.user)) & Q(slug=slug)).exists():
                return List.objects.get((Q(isAdmin = True) | Q(owner = self.request.user)) & Q(slug=slug))
            else:
                raise NotFoundException("The list with the given slug does not exist")
        else:
            if List.objects.filter(Q(owner = self.request.user) & Q(slug=slug)).exists():
                return List.objects.get(Q(owner = self.request.user) & Q(slug=slug))
            else:
                raise NotFoundException("The list with the given slug does not exist")
        
    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page = self.request.GET.get('page',None)
        description = curr_list.description
        public = curr_list.public
        name = curr_list.name
        difficulty = None
        video_link = None
        contest_link = None
        editorial = None
        if ListExtraInfo.objects.filter(curr_list=curr_list).exists():
            qs = ListExtraInfo.objects.get(curr_list=curr_list)
            difficulty = qs.difficulty
            video_link = qs.video_link
            contest_link = qs.contest_link
            editorial = qs.editorial
        page_size = 10
        problem_qs = curr_list.problem.all().order_by('rating','id')

        path = request.build_absolute_uri('/lists/userlist/edit/' + str(slug) + '?')
        cnt = int(curr_list.problem.all().count()/page_size)
        if curr_list.problem.all().count() % page_size != 0:
            cnt += 1
        if page is None:
            page = '1'
        if cnt == 0 :
            return response.Response({'status' : 'OK' , 'result' : []})
        if page.isdigit():
            page = int(page)
        else: 
            return response.Response({'status' : 'FAILED' , 'error' : 'Page must be an integer.'},status=status.HTTP_400_BAD_REQUEST)
        if page > cnt : 
            return response.Response({'status' : 'FAILED' , 'error' : 'Page Out of Bound'},status=status.HTTP_400_BAD_REQUEST)
        if page == cnt :
            Next = None
        else :
            Next = path + 'page='+str(page+1)
        if page == 1:
            Prev = None
        else :
            Prev = path + 'page='+str(page-1)
        qs = getqs(problem_qs,page_size,page)
        return response.Response({
            'status' : "OK",
            'result' : ProblemSerializer(qs,many=True,context = {"slug" : slug,"user" : self.request.user}).data,
            'link' : {
                'first' : path + "page=1",
                'last' : path + "page" + str(cnt),
                'prev' : Prev,
                'next' : Next,
            },
            'meta' : {
                'user' : None,
                'completed' : False,
                'name' : name,
                'description' : description,
                'public' : public,
                'difficulty' : difficulty,
                'video_link' : video_link,
                'contest_link' : contest_link,
                'editorial' : editorial,
                'current_page' : page,
                'from' : (page-1)*page_size + 1,
                'last_page' : cnt,
                'path' : request.build_absolute_uri('/lists/userlist/edit/' + str(slug)),
                'per_page' : page_size,
                'to' : page*page_size,
                'total' : curr_list.problem.all().count()
            }
        })

    def put(self,request,slug):
        curr_list = self.get_object(slug)
        data = request.data
        name = data.get('name',None)
        description = data.get('description',None)
        public = data.get('public',None)
        if name is not None:
            if List.objects.filter(owner=self.request.user,name=name).exists():
                return response.Response({"status" : 'FAILED','error' :"You already have a created a list with the same name "},status=status.HTTP_400_BAD_REQUEST)
            else:
                curr_list.name = name
        if description is not None:
            curr_list.description = description
        if public is not None:
            if public is not True and public is not False:
                return response.Response({"status" : 'FAILED','error' :"public field can only be true or false (with the lowercase initial character)"},status=status.HTTP_400_BAD_REQUEST)
            curr_list.public = public
        if data.get('delete_probs',None):
            for ele in data.get('delete_probs',None):
                prob_id = ele.get('prob_id',None)
                platform = ele.get('platform',None)
                if not Problem.objects.filter(prob_id = prob_id,platform = platform).exists():
                    return response.Response({"status" : 'FAILED','error' :"Problem with the prob_id " + ele + " and platform " + platform + " does not exist"},status=status.HTTP_400_BAD_REQUEST)                 
                curr_prob = Problem.objects.get(prob_id=prob_id,platform = platform)
                if not curr_list.problem.filter(prob_id=prob_id,platform = platform).exists():
                    return response.Response({"status" : 'FAILED','error' :"Problem with the given prob_id " + ele + " does not exists within the list"},status=status.HTTP_400_BAD_REQUEST) 
                curr_list.problem.remove(curr_prob)
        curr_list.save()
        return response.Response({"status" : 'OK','result' :"Userlist has been updated",'slug' : curr_list.slug},status=status.HTTP_200_OK)

    def delete(self,request,slug):
        curr_list = self.get_object(slug)
        curr_list.delete()
        return response.Response({"status" : "OK",'result' : 'list with the given slug deleted'},status=status.HTTP_200_OK)

# class EditUserlistView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [AuthenticatedActivated]
#     serializer_class = EditUserlistSerializer
#     queryset = List.objects.all()
#     lookup_field = 'slug'

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return self.queryset.filter(Q(isAdmin = True) | Q(owner = self.request.user))
#         else:
#             return self.queryset.filter(owner=self.request.user)

#     def get_serializer_context(self,**kwargs):
#         data = super().get_serializer_context(**kwargs)
#         data['user'] = self.request.user.username
#         return data

#     def update(self,request,**kwargs):
#         data = request.data
#         if data.get('delete_probs',None):
#             for ele in data.get('delete_probs',None):
#                 prob_id = ele.get('prob_id',None)
#                 platform = ele.get('platform',None)
#                 if not Problem.objects.filter(prob_id = prob_id,platform = platform).exists():
#                     return response.Response({"status" : 'FAILED','error' :"Problem with the prob_id " + ele + " and platform " + platform + " does not exist"},status=status.HTTP_400_BAD_REQUEST) 
#                 if not List.objects.filter(slug = data['slug']).exists():
#                     return response.Response({"status" : 'FAILED','error' :"List with the provided slug does not exist"},status=status.HTTP_400_BAD_REQUEST)
#                 curr_prob = Problem.objects.get(prob_id=prob_id,platform = platform)
#                 curr_list = List.objects.get(slug=data['slug'])
#                 if not curr_list.problem.filter(prob_id=prob_id,platform = platform).exists():
#                     return response.Response({"status" : 'FAILED','error' :"Problem with the given prob_id " + ele + " does not exists within the list"},status=status.HTTP_400_BAD_REQUEST) 
#                 curr_list.problem.remove(curr_prob)
#         return super().update(request,**kwargs)


class AddProblemsAdminView(generics.GenericAPIView):
    permission_classes = [AuthenticatedAdmin]
    serializer_class = AddProblemsAdminSerializer

    def post(self,request,*args,**kwargs):
        data = request.data
        slug = data.get('slug',None)
        if not slug:
            return response.Response({"status" : 'FAILED','error' :"slug not provided"},status=status.HTTP_400_BAD_REQUEST) 
        if not List.objects.filter(slug=slug).exists(): 
            return response.Response({"status" : 'FAILED','error' :"List with the provided slug does not exist"},status=status.HTTP_400_BAD_REQUEST) 
        curr_list = List.objects.get(slug = slug)
        final = set()
        wrong = set()
        double = set()
        if data.get('prob_id',None):
            for ele in data.get('prob_id',None):
                final.add(ele)
        for ele in final:
            if not Problem.objects.filter(prob_id = ele).exists():
                wrong.add(ele)
                continue
            if Problem.objects.filter(prob_id = ele).count() > 1:
                double.add(ele)
                continue
            if curr_list.problem.filter(prob_id=ele).exists():  
                continue
            curr_prob = Problem.objects.get(prob_id=ele)
            curr_list.problem.add(curr_prob)
        return response.Response({"status" : 'OK','result' :"The correct problems have been inserted in the list",'wrong' : wrong,'double' : double},status=status.HTTP_200_OK)  
            
            