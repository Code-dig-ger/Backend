from rest_framework import generics, status, views, response

from user.models import UserFriends

from .models import List, ListExtraInfo, LadderStarted, ListInfo
from problem.models import Problem
from .serializers import (GetLadderSerializer, GetSerializer, 
                          GetUserlistSerializer, EditUserlistSerializer,
                          CreateUserlistSerializer, ProblemSerializer,
                          UserlistAddSerializer, AddProblemsAdminSerializer,)
from django.db.models import Q, Count, Subquery
from user.permissions import *
from user.exception import *
from .utils import *
from user.models import User


class TopicwiseGetListView(generics.ListAPIView):
    serializer_class = GetSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list='1') | Q(type_list='3'))
                                   & Q(isTopicWise=True) & Q(public=True)
                                   & Q(isAdmin=True))

    def get_serializer_context(self, **kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user
        return data


class TopicWiseRetrieveView(views.APIView):
    permission_classes = [AuthenticatedOrReadOnly]

    def get_object(self, slug):
        if List.objects.filter((Q(type_list='1') | Q(type_list='3'))
                               & Q(isTopicWise=True) & Q(public=True)
                               & Q(isAdmin=True) & Q(slug=slug)).exists():
            return List.objects.get(slug=slug)
        raise NotFoundException("The list with the given slug does not exist")

    def get(self, request, slug):
        curr_list = self.get_object(slug)
        page_number = self.request.GET.get('page', None)
        page_size = self.request.GET.get('pageSize', '6')

        if page_size.isdigit():
            page_size = int(page_size)
        else:
            raise ValidationException('Page Size must be an integer')

        problem_qs = curr_list.problem.all().order_by('rating', 'id')
        total_problems = problem_qs.count()
        if total_problems == 0:
            return response.Response({'status': 'OK', 'result': []})

        url = request.build_absolute_uri('/lists/topicwise/list/' + str(slug))
        user = self.request.user
        if user.is_anonymous:
            user = None

        if not page_number:
            page_number, unsolved_prob, isCompleted = \
                            get_unsolved_page_number(problem_qs, user, page_size)
        else:
            isCompleted = False
            if page_number.isdigit():
                page_number = int(page_number)
            else:
                raise ValidationException('Page must be an integer')
            total_page = get_total_page(total_problems, page_size)
            if page_number > total_page:
                raise ValidationException('Page Out of Bound')
            update_page_submission(problem_qs, user, page_size, page_number)

        res = get_response_dict(curr_list, user, page_number, page_size, url,
                                problem_qs, isCompleted)
        return response.Response(res)


class TopicwiseGetLadderView(generics.ListAPIView):
    serializer_class = GetLadderSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list='2') | Q(type_list='3'))
                                   & Q(isTopicWise=True) & Q(public=True)
                                   & Q(isAdmin=True))

    def get_serializer_context(self, **kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user
        return data


class TopicWiseLadderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AuthenticatedOrReadOnly]

    def get_object(self, slug):
        if List.objects.filter((Q(type_list='2') | Q(type_list='3'))
                               & Q(isTopicWise=True) & Q(public=True)
                               & Q(isAdmin=True) & Q(slug=slug)).exists():
            return List.objects.get(slug=slug)
        raise NotFoundException("The list with the given slug does not exist")

    def get(self, request, slug):
        curr_list = self.get_object(slug)
        page_number = self.request.GET.get('page', None)
        page_size = self.request.GET.get('pageSize', '6')

        if page_size.isdigit():
            page_size = int(page_size)
        else:
            raise ValidationException('Page Size must be an integer')

        url = request.build_absolute_uri('/lists/topicwise/ladder/' +
                                         str(slug))

        user = self.request.user
        if user.is_anonymous:
            user = None

        if user is not None:
            if not LadderStarted.objects.filter(ladder_user=user,
                                                ladder=curr_list).exists():
                LadderStarted.objects.create(ladder_user=user,
                                             ladder=curr_list)

        problem_qs = curr_list.problem.all()
        if user:
            p = get_list_platform(user)
            problem_qs = problem_qs.filter(platform__in=p)

        total_problems = problem_qs.count()
        if total_problems == 0:
            return response.Response({'status': 'OK', 'result': []})

        problem_qs = problem_qs.order_by('rating', 'id')
        unsolved_prob = None
        unsolved_page = None
        isCompleted = False

        if user:
            unsolved_page, unsolved_prob, isCompleted = \
                    get_unsolved_page_number(problem_qs, user, page_size)

        if page_number:
            isCompleted = False
            if page_number.isdigit():
                page_number = int(page_number)
            else:
                raise ValidationException('Page must be an integer')
            total_page = get_total_page(total_problems, page_size)
            if page_number > total_page:
                raise ValidationException('Page Out of Bound')
        else:
            page_number = unsolved_page if unsolved_page else 1

        res = get_response_dict(curr_list, user, page_number, page_size, url,
                                problem_qs, isCompleted, unsolved_page,
                                unsolved_prob)
        return response.Response(res)


class LevelwiseGetListView(generics.ListAPIView):
    serializer_class = GetSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list='1') | Q(type_list='3'))
                                   & Q(isTopicWise=False) & Q(public=True)
                                   & Q(isAdmin=True))

    def get_serializer_context(self, **kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user
        return data


class LevelwiseRetrieveView(views.APIView):
    permission_classes = [AuthenticatedOrReadOnly]

    def get_object(self, slug):
        if List.objects.filter((Q(type_list='1') | Q(type_list='3'))
                               & Q(isTopicWise=False) & Q(public=True)
                               & Q(isAdmin=True) & Q(slug=slug)).exists():
            return List.objects.get(slug=slug)
        raise NotFoundException("The list with the given slug does not exist")

    def get(self, request, slug):
        curr_list = self.get_object(slug)
        page_number = self.request.GET.get('page', None)
        page_size = self.request.GET.get('pageSize', '6')

        if page_size.isdigit():
            page_size = int(page_size)
        else:
            raise ValidationException('Page Size must be an integer')

        problem_qs = curr_list.problem.all().order_by('rating', 'id')
        total_problems = problem_qs.count()
        if total_problems == 0:
            return response.Response({'status': 'OK', 'result': []})

        url = request.build_absolute_uri('/lists/levelwise/list/' + str(slug))
        user = self.request.user
        if user.is_anonymous:
            user = None

        if not page_number:
            page_number, unsolved_prob, isCompleted = \
                            get_unsolved_page_number(problem_qs, user, page_size)
        else:
            isCompleted = False
            if page_number.isdigit():
                page_number = int(page_number)
            else:
                raise ValidationException('Page must be an integer')
            total_page = get_total_page(total_problems, page_size)
            if page_number > total_page:
                raise ValidationException('Page Out of Bound')
            update_page_submission(problem_qs, user, page_size, page_number)

        res = get_response_dict(curr_list, user, page_number, page_size, url,
                                problem_qs, isCompleted)
        return response.Response(res)


class LevelwiseGetLadderView(generics.ListAPIView):
    serializer_class = GetLadderSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list='2') | Q(type_list='3'))
                                   & Q(isTopicWise=False) & Q(public=True)
                                   & Q(isAdmin=True))

    def get_serializer_context(self, **kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user
        return data


class LevelwiseLadderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AuthenticatedOrReadOnly]

    def get_object(self, slug):
        if List.objects.filter((Q(type_list='2') | Q(type_list='3'))
                               & Q(isTopicWise=False) & Q(public=True)
                               & Q(isAdmin=True) & Q(slug=slug)).exists():
            return List.objects.get(slug=slug)
        raise NotFoundException("The list with the given slug does not exist")

    def get(self, request, slug):
        curr_list = self.get_object(slug)
        page_number = self.request.GET.get('page', None)
        page_size = self.request.GET.get('pageSize', '6')

        if page_size.isdigit():
            page_size = int(page_size)
        else:
            raise ValidationException('Page Size must be an integer')

        url = request.build_absolute_uri('/lists/levelwise/ladder/' +
                                         str(slug))

        user = self.request.user
        if user.is_anonymous:
            user = None

        if user is not None:
            if not LadderStarted.objects.filter(ladder_user=user,
                                                ladder=curr_list).exists():
                LadderStarted.objects.create(ladder_user=user,
                                             ladder=curr_list)

        problem_qs = curr_list.problem.all()
        if user:
            p = get_list_platform(user)
            problem_qs = problem_qs.filter(platform__in=p)

        total_problems = problem_qs.count()
        if total_problems == 0:
            return response.Response({'status': 'OK', 'result': []})

        problem_qs = problem_qs.order_by('rating', 'id')
        unsolved_prob = None
        unsolved_page = None
        isCompleted = False

        if user:
            unsolved_page, unsolved_prob, isCompleted = \
                    get_unsolved_page_number(problem_qs, user, page_size)

        if page_number:
            isCompleted = False
            if page_number.isdigit():
                page_number = int(page_number)
            else:
                raise ValidationException('Page must be an integer')
            total_page = get_total_page(total_problems, page_size)
            if page_number > total_page:
                raise ValidationException('Page Out of Bound')
        else:
            page_number = unsolved_page if unsolved_page else 1

        res = get_response_dict(curr_list, user, page_number, page_size, url,
                                problem_qs, isCompleted, unsolved_page,
                                unsolved_prob)
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
            qs = List.objects.filter(
                Q(owner=self.request.user) | Q(isAdmin=True))
            return qs
        else:
            qs = List.objects.filter(owner=self.request.user)
            return qs


class ListGetView(generics.ListAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = GetUserlistSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
        except:
            raise ValidationException('User with given Username not exists.')

        if self.request.user.is_authenticated and username == self.request.user.username:
            qs = List.objects.filter(owner=self.request.user)
        else:
            qs = List.objects.filter(Q(owner=user) & Q(public=True))
        return qs
    
    def get(self,request,username):
        qs = self.get_queryset()
        send_data = GetUserlistSerializer(qs, many=True).data
        return response.Response({'status':'OK','result':send_data})

class ListStats(generics.ListAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = GetUserlistSerializer

    def get(self, request, slug):
        try:
            list = List.objects.get(slug=slug)
        except:
            raise ValidationException(
                "List with the provided slug does not exist")
        qs = ListInfo.objects.filter(p_list=list)
        send_data = ProblemSerializer(qs,many=True).data
        return response.Response({'status':'OK','result':send_data})

class UserStandingStats(generics.ListAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = GetUserlistSerializer

    def get(self,request,slug):
        here = self.request.user
        friend = self.request.GET.get('friend',False)
        try:
            user = User.objects.get(username=here)
        except:
            raise ValidationException('User with given Username not exists.')
        try:
            list = List.objects.get(slug=slug)
        except:
            raise ValidationException(
                "List with the provided slug does not exist")
        
        if here!=list.owner and list.public==False:
            raise ValidationException("The list must be public")
        qs = Solved.objects.filter(
            problem__in=Subquery(ListInfo.objects.filter(p_list=list).values('problem'))
            ).values('user').annotate(problems_solved=Count('user')).order_by('-problems_solved')

        if friend:
            qs = qs.filter(user__in=Subquery(UserFriends.objects.filter(from_user=user).values('to_user_id')))
        send_data = []
        for rank,q in enumerate(qs):
            send_data.append({
                'user': q.get('user',None),
                'rank': rank+1,
                'problems_solved': q.get('problems_solved',None)
            })
        return response.Response({'status':'OK','result':send_data})


class UserlistCreateView(generics.CreateAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = CreateUserlistSerializer

    def get_serializer_context(self, **kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class UserlistAddProblemView(generics.CreateAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = UserlistAddSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        here = self.request.user
        prob_id = data.get('prob_id', None)
        slug = data.get('slug', None)
        platform = data.get('platform', None)
        if prob_id is None or slug is None or platform is None:
            raise ValidationException(
                "prob_id or slug or platform not provided")
        if not List.objects.filter(slug=slug).exists():
            raise ValidationException(
                "List with the provided slug does not exist")
        if not Problem.objects.filter(prob_id=prob_id,
                                      platform=platform).exists():
            raise ValidationException(
                "Problem with the given prob_id and platform does not exist")
        curr_list = List.objects.get(slug=slug)
        curr_prob = Problem.objects.get(prob_id=prob_id, platform=platform)
        if curr_list.problem.filter(prob_id=prob_id,
                                    platform=platform).exists():
            raise ValidationException(
                "Problem with the given prob_id and platform already exists within the list"
            )
        if curr_list.owner != here:
            raise ValidationException(
                "Only the owner of the list can add problems to this list")
        curr_list.problem.add(curr_prob)
        return response.Response(
            {
                "status": 'OK',
                'result': "Given problem has been added to the list"
            },
            status=status.HTTP_200_OK)


class EditUserlistView(generics.GenericAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = EditUserlistSerializer

    def get_object(self, slug):
        if self.request.user.is_staff:
            if List.objects.filter((Q(isAdmin=True)
                                    | Q(owner=self.request.user))
                                   & Q(slug=slug)).exists():
                return List.objects.get((Q(isAdmin=True)
                                         | Q(owner=self.request.user))
                                        & Q(slug=slug))
            else:
                raise NotFoundException(
                    "The list with the given slug does not exist")
        else:
            if List.objects.filter(Q(owner=self.request.user)
                                   & Q(slug=slug)).exists():
                return List.objects.get(
                    Q(owner=self.request.user) & Q(slug=slug))
            else:
                raise NotFoundException(
                    "The list with the given slug does not exist")

    def get(self, request, slug):
        curr_list = self.get_object(slug)
        page = self.request.GET.get('page', None)
        page_size = self.request.GET.get('per_page', 10)
        problem_qs = curr_list.problem.all().order_by('rating', 'id')

        cnt = int(curr_list.problem.all().count() / page_size)
        if curr_list.problem.all().count() % page_size != 0:
            cnt += 1
        if page is None:
            page = '1'
        if cnt == 0:
            return response.Response({'status': 'OK', 'result': []})
        if page.isdigit():
            page = int(page)
        else:
            raise ValidationException("Page must be an integer.")
        if page > cnt:
            raise ValidationException("Page Out of Bound")
        url = request.build_absolute_uri('/lists/userlist/edit/' + str(slug))
        res = get_response_dict(curr_list, self.request.user, page, page_size,
                                url, problem_qs)
        return response.Response(res)

    def put(self, request, slug):
        curr_list = self.get_object(slug)
        data = request.data
        name = data.get('name', None)
        description = data.get('description', None)
        public = data.get('public', None)
        if name is not None:
            if List.objects.filter(owner=self.request.user,
                                   name=name).exists():
                raise ValidationException(
                    "You already have a created a list with the same name.")
            else:
                curr_list.name = name
        if description is not None:
            curr_list.description = description
        if public is not None:
            if public is not True and public is not False:
                raise ValidationException(
                    "public field can only be true or false (with the lowercase initial character)"
                )
            if curr_list.public == True and public == False:
                raise ValidationException(
                    "A list once made public cannot be made private again")
            curr_list.public = public
        if data.get('delete_probs', None):
            for ele in data.get('delete_probs', None):
                prob_id = ele.get('prob_id', None)
                platform = ele.get('platform', None)
                if not Problem.objects.filter(prob_id=prob_id,
                                              platform=platform).exists():
                    raise ValidationException(
                        "Problem with the given prob_id {} \
                        does not exists within the list".format(ele))
                curr_prob = Problem.objects.get(prob_id=prob_id,
                                                platform=platform)
                if not curr_list.problem.filter(prob_id=prob_id,
                                                platform=platform).exists():
                    raise ValidationException(
                        "Problem with the given prob_id {} \
                        does not exists within the list".format(ele))
                curr_list.problem.remove(curr_prob)
        curr_list.save()
        return response.Response(
            {
                "status": 'OK',
                'result': "Userlist has been updated",
                'slug': curr_list.slug
            },
            status=status.HTTP_200_OK)

    def delete(self, request, slug):
        curr_list = self.get_object(slug)
        curr_list.delete()
        return response.Response(
            {
                "status": "OK",
                'result': 'list with the given slug deleted'
            },
            status=status.HTTP_200_OK)


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

    def post(self, request, *args, **kwargs):
        data = request.data
        slug = data.get('slug', None)
        l = data.get('l', 0)
        r = data.get('r', 5000)
        if not slug:
            raise ValidationException("slug not provided")
        if not List.objects.filter(slug=slug).exists():
            raise ValidationException(
                "List with the provided slug does not exist")
        curr_list = List.objects.get(slug=slug)
        final = set()
        wrong = set()
        double = set()
        rating_l = set()
        rating_r = set()
        if data.get('prob_id', None):
            for ele in data.get('prob_id', None):
                final.add(ele)
        for ele in final:
            if not Problem.objects.filter(prob_id=ele).exists():
                wrong.add(ele)
                continue
            if Problem.objects.filter(prob_id=ele).count() > 1:
                double.add(ele)
                continue
            if curr_list.problem.filter(prob_id=ele).exists():
                continue
            curr_prob = Problem.objects.get(prob_id=ele)
            if curr_prob.rating <= l:
                rating_l.add(ele)
            elif curr_prob.rating > r:
                rating_r.add(ele)
            else:
                curr_list.problem.add(curr_prob)
        return response.Response(
            {
                "status": 'OK',
                'result':
                "The correct problems have been inserted in the list",
                'wrong': wrong,
                'double': double,
                'rating_l': rating_l,
                'rating_r': rating_r
            },
            status=status.HTTP_200_OK)


from .cron import updater
from django.http import JsonResponse


def testing(request):
    updater()
    return JsonResponse({'status': 'OK'})
