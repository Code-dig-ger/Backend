from rest_framework import generics,status,permissions,views,response,mixins
from .models import ListInfo,Solved,List
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
    UpdateListSerializer
)
from django.db.models import Q
from .permissions import IsOwner
from .solved_update import codeforces,uva,atcoder,codechef,spoj
from .cron import updater,cron_atcoder,cron_codechef,cron_codeforces,cron_spoj,cron_uva,codechef_list
from django.core.paginator import Paginator
from django.http import Http404
from user.permissions import *


class TopicwiseGetListView(generics.ListAPIView):
    serializer_class=GetSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True) & Q(public=True) & Q(owner__is_staff=True))

class TopicWiseRetrieveView(views.APIView):
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True)  & Q(public=True) & Q(owner__is_staff=True))
    
    def get_object(self,slug):
        if List.objects.filter(slug=slug).exists():
            return List.objects.get(slug=slug)
        return Http404

    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page = self.request.GET.get('page',None)
        page_size = 6
        paginator = Paginator(curr_list.problem.all().order_by('rating'),page_size)
        cnt = int(curr_list.problem.all().count()/page_size)
        if curr_list.problem.all().count() % page_size != 0:
            cnt += 1
        path = request.build_absolute_uri('/lists/topicwise/list/' + str(slug) + '/?')
        user = self.request.user
        if user.is_anonymous:
            user = None
        else:
            user = user.username
        if not page:
            if cnt == 0 :
                return response.Response({'status' : 'OK' , 'result' : []})
            for prob in curr_list.problem.all():
                if Solved.objects.filter(user__username=user,problem=prob).exists():
                    continue
                if prob.platform == 'F':
                    codeforces(user)
                elif prob.platform == 'A':
                    atcoder(user)
                elif prob.platform == 'U':
                    uva(user)
                elif prob.platform == 'S':
                    spoj(user,prob.prob_id)
                elif prob.platform == 'C':
                    codechef(user,prob.prob_id) 
            page = 1
            while page <= cnt:
                qs = paginator.page(page)
                for ele in qs:
                    solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                    if not solve.exists():
                        if page == cnt :
                            Next = None
                        else :
                            Next = path + 'page='+str(page+1)
                        if page == 1:
                            Prev = None
                        else :
                            Prev = path + 'page='+str(page-1)
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
                                'user' : user,
                                'completed' : False,
                                'current_page' : page,
                                'from' : (page-1)*page_size + 1,
                                'last_page' : cnt,
                                'path' : request.build_absolute_uri('/lists/topicwise/list/' + str(slug) + '/'),
                                'per_page' : page_size,
                                'to' : page*page_size,
                                'total' : curr_list.problem.all().count()
                            }
                        })
                page += 1
            page = 1
            qs = paginator.page(page)
            if page == cnt :
                Next = None
            else :
                Next = path + 'page='+str(page+1)
            if page == 1:
                Prev = None
            else :
                Prev = path + 'page='+str(page-1)
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
                    'user' : user,
                    'completed' : True,
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/topicwise/list/' + str(slug) + '/'),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : curr_list.problem.all().count()
                }
            })
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
            qs = paginator.page(page)
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
                    'user' : user,
                    'completed' : False,
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/topicwise/list/' + str(slug) + '/'),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : curr_list.problem.all().count()
                }
            })


class TopicwiseGetLadderView(generics.ListAPIView):
    serializer_class=GetLadderSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = True)  & Q(public=True) & Q(owner__is_staff=True))


class TopicWiseLadderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True)  & Q(public=True) & Q(owner__is_staff=True))
    
    def get_object(self,slug):
        if List.objects.filter(slug=slug).exists():
            return List.objects.get(slug=slug)
        return Http404
    
    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page = self.request.GET.get('page',None)
        page_size = 6
        path = request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '/?')
        user = self.request.user
        if not user.is_anonymous:
            user = user.username
            tspoj = Profile.objects.get(owner__username = user).spoj
            tuva = Profile.objects.get(owner__username = user).uva_handle
            tcodeforces = Profile.objects.get(owner__username = user).codeforces
            tcodechef = Profile.objects.get(owner__username = user).codechef
            tatcoder = Profile.objects.get(owner__username = user).atcoder
            temp = []
            if tspoj is None:
                temp.append('S')
            if tuva is None:
                temp.append('U')
            if tatcoder is None:
                temp.append('A')
            if tcodechef is None:
                temp.append('C')
            final = None
            prev = None
            for ele in temp:
                if prev is None:
                    prev = curr_list.problem.all().exclude(platform=ele)
                    final = prev
                else:
                    chain1 = prev.exclude(platform=ele)
                    prev = chain1
                    final = prev
            if not page:
                if final is None:
                    cnt = int(curr_list.problem.all().count()/page_size)
                    if curr_list.problem.all().count() % page_size != 0:
                        cnt += 1
                    if cnt == 0 :
                        return response.Response({'status' : 'OK' , 'result' : []})
                    paginator = Paginator(curr_list.problem.all().order_by('rating'),page_size)
                    for prob in curr_list.problem.all():
                        if Solved.objects.filter(user__username=user,problem=prob).exists():
                            continue
                        if prob.platform == 'F':
                            codeforces(user)
                        elif prob.platform == 'A':
                            atcoder(user)
                        elif prob.platform == 'U':
                            uva(user)
                        elif prob.platform == 'S':
                            spoj(user,prob.prob_id)
                        elif prob.platform == 'C':
                            codechef(user,prob.prob_id) 
                    page = 1
                    while page <= cnt:
                        qs = paginator.page(page)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                            if not solve.exists():
                                if page == cnt :
                                    Next = None
                                else :
                                    Next = path + 'page='+str(page+1)
                                if page == 1:
                                    Prev = None
                                else :
                                    Prev = path + 'page='+str(page-1)
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
                                        'user' : user,
                                        'curr_prob' : ele.prob_id,
                                        'completed' : False,
                                        'current_page' : page,
                                        'from' : (page-1)*page_size + 1,
                                        'last_page' : cnt,
                                        'path' : request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '/'),
                                        'per_page' : page_size,
                                        'to' : page*page_size,
                                        'total' : curr_list.problem.all().count()
                                    }
                                })
                        page += 1
                    page = 1
                    qs = paginator.page(page)
                    if page == cnt :
                        Next = None
                    else :
                        Next = path + 'page='+str(page+1)
                    if page == 1:
                        Prev = None
                    else :
                        Prev = path + 'page='+str(page-1)
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
                            'user' : user,
                            'curr_prob' : None,
                            'completed' : True,
                            'current_page' : page,
                            'from' : (page-1)*page_size + 1,
                            'last_page' : cnt,
                            'path' : request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '/'),
                            'per_page' : page_size,
                            'to' : page*page_size,
                            'total' : curr_list.problem.all().count()
                        }
                    })
                else:
                    cnt = int(final.count()/page_size)
                    if final.count() % page_size != 0:
                        cnt += 1
                    if cnt == 0 :
                        return response.Response({'status' : 'OK' , 'result' : []})
                    paginator = Paginator(final.order_by('rating'),page_size)  
                    for prob in final:
                        if Solved.objects.filter(user__username=user,problem=prob).exists():
                            continue
                        if prob.platform == 'F':
                            codeforces(user)
                        elif prob.platform == 'A':
                            atcoder(user)
                        elif prob.platform == 'U':
                            uva(user)
                        elif prob.platform == 'S':
                            spoj(user,prob.prob_id)
                        elif prob.platform == 'C':
                            codechef(user,prob.prob_id) 
                    page = 1
                    while page <= cnt:
                        qs = paginator.page(page)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                            if not solve.exists():
                                if page == cnt :
                                    Next = None
                                else :
                                    Next = path + 'page='+str(page+1)
                                if page == 1:
                                    Prev = None
                                else :
                                    Prev = path + 'page='+str(page-1)
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
                                        'user' : user,
                                        'curr_prob' : ele.prob_id,
                                        'completed' : False,
                                        'current_page' : page,
                                        'from' : (page-1)*page_size + 1,
                                        'last_page' : cnt,
                                        'path' : request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '/'),
                                        'per_page' : page_size,
                                        'to' : page*page_size,
                                        'total' : final.count()
                                    }
                                })
                        page += 1 
                    page = 1
                    qs = paginator.page(page)
                    if page == cnt :
                        Next = None
                    else :
                        Next = path + 'page='+str(page+1)
                    if page == 1:
                        Prev = None
                    else :
                        Prev = path + 'page='+str(page-1)
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
                            'user' : user,
                            'curr_prob' : None,
                            'completed' : True,
                            'current_page' : page,
                            'from' : (page-1)*page_size + 1,
                            'last_page' : cnt,
                            'path' : request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '/'),
                            'per_page' : page_size,
                            'to' : page*page_size,
                            'total' : final.count()
                        }
                    })
            else:
                latest_unsolved = None 
                if final is None:
                    cnt = int(curr_list.problem.all().count()/page_size)
                    if curr_list.problem.all().count() % page_size != 0:
                        cnt += 1
                    paginator = Paginator(curr_list.problem.all().order_by('rating'),page_size)
                    start = 1
                    while start <= cnt:
                        qs = paginator.page(start)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                            if not solve.exists():
                                latest_unsolved = ele.prob_id
                                break
                        start += 1
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
                    qs = paginator.page(page)
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
                            'user' : user,
                            'completed' : False,
                            'curr_prob' : latest_unsolved,
                            'current_page' : page,
                            'from' : (page-1)*page_size + 1,
                            'last_page' : cnt,
                            'path' : request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '/'),
                            'per_page' : page_size,
                            'to' : page*page_size,
                            'total' : curr_list.problem.all().count()
                        }
                    })
                else:
                    paginator = Paginator(final.order_by('rating'),page_size) 
                    cnt = int(final.count()/page_size)
                    if final.count() % page_size != 0:
                        cnt += 1
                    start = 1
                    while start <= cnt:
                        qs = paginator.page(start)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                            if not solve.exists():
                                latest_unsolved = ele.prob_id
                                break
                        start += 1
                    cnt = int(final.count()/page_size)
                    if final.count() % page_size != 0:
                        cnt += 1
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
                    qs = paginator.page(page)
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
                            'user' : user,
                            'completed' : False,
                            'curr_prob' : latest_unsolved,
                            'current_page' : page,
                            'from' : (page-1)*page_size + 1,
                            'last_page' : cnt,
                            'path' : request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '/'),
                            'per_page' : page_size,
                            'to' : page*page_size,
                            'total' : final.count()
                        }
                    })
        else:
            paginator = Paginator(curr_list.problem.all().order_by('rating'),page_size)
            cnt = int(curr_list.problem.all().count()/page_size)
            if curr_list.problem.all().count() % page_size != 0:
                cnt += 1
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
            qs = paginator.page(page)
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
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/topicwise/ladder/' + str(slug) + '/'),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : curr_list.problem.all().count()
                }
            })

class LevelwiseGetListView(generics.ListAPIView):
    serializer_class=GetSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True) & Q(owner__is_staff=True))


class LevelwiseRetrieveView(views.APIView):
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True) & Q(owner__is_staff=True))
    
    def get_object(self,slug):
        if List.objects.filter(slug=slug).exists():
            return List.objects.get(slug=slug)
        return Http404

    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page = self.request.GET.get('page',None)
        page_size = 6
        paginator = Paginator(curr_list.problem.all().order_by('rating'),page_size)
        cnt = int(curr_list.problem.all().count()/page_size)
        if curr_list.problem.all().count() % page_size != 0:
            cnt += 1
        path = request.build_absolute_uri('/lists/levelwise/list/' + str(slug) + '/?')
        user = self.request.user
        if user.is_anonymous:
            user = None
        if not page:
            if cnt == 0 :
                return response.Response({'status' : 'OK' , 'result' : []})
            for prob in curr_list.problem.all():
                if Solved.objects.filter(user__username=user,problem=prob).exists():
                    continue
                if prob.platform == 'F':
                    codeforces(user)
                elif prob.platform == 'A':
                    atcoder(user)
                elif prob.platform == 'U':
                    uva(user)
                elif prob.platform == 'S':
                    spoj(user,prob.prob_id)
                elif prob.platform == 'C':
                    codechef(user,prob.prob_id) 
            page = 1
            while page <= cnt:
                qs = paginator.page(page)
                for ele in qs:
                    solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                    if not solve.exists():
                        if page == cnt :
                            Next = None
                        else :
                            Next = path + 'page='+str(page+1)
                        if page == 1:
                            Prev = None
                        else :
                            Prev = path + 'page='+str(page-1)
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
                                'user' : user,
                                'completed' : False,
                                'current_page' : page,
                                'from' : (page-1)*page_size + 1,
                                'last_page' : cnt,
                                'path' : request.build_absolute_uri('/lists/levelwise/list/' + str(slug) + '/'),
                                'per_page' : page_size,
                                'to' : page*page_size,
                                'total' : curr_list.problem.all().count()
                            }
                        })
                page += 1
            page = 1
            qs = paginator.page(page)
            if page == cnt :
                Next = None
            else :
                Next = path + 'page='+str(page+1)
            if page == 1:
                Prev = None
            else :
                Prev = path + 'page='+str(page-1)
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
                    'user' : user,
                    'completed' : True,
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/levelwise/list/' + str(slug) + '/'),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : curr_list.problem.all().count()
                }
            })
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
            qs = paginator.page(page)
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
                    'user' : user,
                    'completed' : False,
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/levelwise/list/' + str(slug) + '/'),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : curr_list.problem.all().count()
                }
            })


class LevelwiseGetLadderView(generics.ListAPIView):
    serializer_class=GetLadderSerializer
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True) & Q(owner__is_staff=True))


class LevelwiseLadderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True) & Q(owner__is_staff=True))
    
    def get_object(self,slug):
        if List.objects.filter(slug=slug).exists():
            return List.objects.get(slug=slug)
        return Http404
    
    def get(self,request,slug):
        curr_list = self.get_object(slug)
        page = self.request.GET.get('page',None)
        page_size = 6
        path = request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '/?')
        user = self.request.user
        if not user.is_anonymous:
            user = user.username
            tspoj = Profile.objects.get(owner__username = user).spoj
            tuva = Profile.objects.get(owner__username = user).uva_handle
            tcodeforces = Profile.objects.get(owner__username = user).codeforces
            tcodechef = Profile.objects.get(owner__username = user).codechef
            tatcoder = Profile.objects.get(owner__username = user).atcoder
            temp = []
            if tspoj is None:
                temp.append('S')
            if tuva is None:
                temp.append('U')
            if tatcoder is None:
                temp.append('A')
            if tcodechef is None:
                temp.append('C')
            final = None
            prev = None
            for ele in temp:
                if prev is None:
                    prev = curr_list.problem.all().exclude(platform=ele)
                    final = prev
                else:
                    chain1 = prev.exclude(platform=ele)
                    prev = chain1
                    final = prev
            if not page:
                if final is None:
                    cnt = int(curr_list.problem.all().count()/page_size)
                    if curr_list.problem.all().count() % page_size != 0:
                        cnt += 1
                    if cnt == 0 :
                        return response.Response({'status' : 'OK' , 'result' : []})
                    paginator = Paginator(curr_list.problem.all().order_by('rating'),page_size)
                    for prob in curr_list.problem.all():
                        if Solved.objects.filter(user__username=user,problem=prob).exists():
                            continue
                        if prob.platform == 'F':
                            codeforces(user)
                        elif prob.platform == 'A':
                            atcoder(user)
                        elif prob.platform == 'U':
                            uva(user)
                        elif prob.platform == 'S':
                            spoj(user,prob.prob_id)
                        elif prob.platform == 'C':
                            codechef(user,prob.prob_id) 
                    page = 1
                    while page <= cnt:
                        qs = paginator.page(page)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                            if not solve.exists():
                                if page == cnt :
                                    Next = None
                                else :
                                    Next = path + 'page='+str(page+1)
                                if page == 1:
                                    Prev = None
                                else :
                                    Prev = path + 'page='+str(page-1)
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
                                        'user' : user,
                                        'curr_prob' : ele.prob_id,
                                        'completed' : False,
                                        'current_page' : page,
                                        'from' : (page-1)*page_size + 1,
                                        'last_page' : cnt,
                                        'path' : request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '/'),
                                        'per_page' : page_size,
                                        'to' : page*page_size,
                                        'total' : curr_list.problem.all().count()
                                    }
                                })
                        page += 1
                    page = 1
                    qs = paginator.page(page)
                    if page == cnt :
                        Next = None
                    else :
                        Next = path + 'page='+str(page+1)
                    if page == 1:
                        Prev = None
                    else :
                        Prev = path + 'page='+str(page-1)
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
                            'user' : user,
                            'curr_prob' : None,
                            'completed' : True,
                            'current_page' : page,
                            'from' : (page-1)*page_size + 1,
                            'last_page' : cnt,
                            'path' : request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '/'),
                            'per_page' : page_size,
                            'to' : page*page_size,
                            'total' : curr_list.problem.all().count()
                        }
                    })
                else:
                    cnt = int(final.count()/page_size)
                    if final.count() % page_size != 0:
                        cnt += 1
                    if cnt == 0 :
                        return response.Response({'status' : 'OK' , 'result' : []})
                    paginator = Paginator(final.order_by('rating'),page_size)  
                    for prob in final:
                        if Solved.objects.filter(user__username=user,problem=prob).exists():
                            continue
                        if prob.platform == 'F':
                            codeforces(user)
                        elif prob.platform == 'A':
                            atcoder(user)
                        elif prob.platform == 'U':
                            uva(user)
                        elif prob.platform == 'S':
                            spoj(user,prob.prob_id)
                        elif prob.platform == 'C':
                            codechef(user,prob.prob_id) 
                    page = 1
                    while page <= cnt:
                        qs = paginator.page(page)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                            if not solve.exists():
                                if page == cnt :
                                    Next = None
                                else :
                                    Next = path + 'page='+str(page+1)
                                if page == 1:
                                    Prev = None
                                else :
                                    Prev = path + 'page='+str(page-1)
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
                                        'user' : user,
                                        'curr_prob' : ele.prob_id,
                                        'completed' : False,
                                        'current_page' : page,
                                        'from' : (page-1)*page_size + 1,
                                        'last_page' : cnt,
                                        'path' : request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '/'),
                                        'per_page' : page_size,
                                        'to' : page*page_size,
                                        'total' : final.count()
                                    }
                                })
                        page += 1 
                    page = 1
                    qs = paginator.page(page)
                    if page == cnt :
                        Next = None
                    else :
                        Next = path + 'page='+str(page+1)
                    if page == 1:
                        Prev = None
                    else :
                        Prev = path + 'page='+str(page-1)
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
                            'user' : user,
                            'curr_prob' : None,
                            'completed' : True,
                            'current_page' : page,
                            'from' : (page-1)*page_size + 1,
                            'last_page' : cnt,
                            'path' : request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '/'),
                            'per_page' : page_size,
                            'to' : page*page_size,
                            'total' : final.count()
                        }
                    })
            else:
                latest_unsolved = None 
                if final is None:
                    cnt = int(curr_list.problem.all().count()/page_size)
                    if curr_list.problem.all().count() % page_size != 0:
                        cnt += 1
                    paginator = Paginator(curr_list.problem.all().order_by('rating'),page_size)
                    start = 1
                    while start <= cnt:
                        qs = paginator.page(start)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                            if not solve.exists():
                                latest_unsolved = ele.prob_id
                                break
                        start += 1
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
                    qs = paginator.page(page)
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
                            'user' : user,
                            'completed' : False,
                            'curr_prob' : latest_unsolved,
                            'current_page' : page,
                            'from' : (page-1)*page_size + 1,
                            'last_page' : cnt,
                            'path' : request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '/'),
                            'per_page' : page_size,
                            'to' : page*page_size,
                            'total' : curr_list.problem.all().count()
                        }
                    })
                else:
                    paginator = Paginator(final.order_by('rating'),page_size) 
                    cnt = int(final.count()/page_size)
                    if final.count() % page_size != 0:
                        cnt += 1
                    start = 1
                    while start <= cnt:
                        qs = paginator.page(start)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=self.request.user,problem=ele)
                            if not solve.exists():
                                latest_unsolved = ele.prob_id
                                break
                        start += 1
                    cnt = int(final.count()/page_size)
                    if final.count() % page_size != 0:
                        cnt += 1
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
                    qs = paginator.page(page)
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
                            'user' : user,
                            'completed' : False,
                            'curr_prob' : latest_unsolved,
                            'current_page' : page,
                            'from' : (page-1)*page_size + 1,
                            'last_page' : cnt,
                            'path' : request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '/'),
                            'per_page' : page_size,
                            'to' : page*page_size,
                            'total' : final.count()
                        }
                    })
        else:
            paginator = Paginator(curr_list.problem.all().order_by('rating'),page_size)
            cnt = int(curr_list.problem.all().count()/page_size)
            if curr_list.problem.all().count() % page_size != 0:
                cnt += 1
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
            qs = paginator.page(page)
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
                    'current_page' : page,
                    'from' : (page-1)*page_size + 1,
                    'last_page' : cnt,
                    'path' : request.build_absolute_uri('/lists/levelwise/ladder/' + str(slug) + '/'),
                    'per_page' : page_size,
                    'to' : page*page_size,
                    'total' : curr_list.problem.all().count()
                }
            })


class updateLadderview(generics.GenericAPIView):
    serializer_class = UpdateLadderSerializer

    def post(self,request,*args, **kwargs):
        prob_id = self.request.GET.get('prob_id')
        if prob_id == None:
            codeforces(self.request.user.username)
            uva(self.request.user.username)
            atcoder(self.request.user.username)
        else:
            if Problem.objects.filter(prob_id=prob_id,platform='F').exists():
                codeforces(self.request.user.username)
            if Problem.objects.filter(prob_id=prob_id,platform='U').exists():
                uva(self.request.user.username)
            if Problem.objects.filter(prob_id=prob_id,platform='A').exists():
                atcoder(self.request.user.username)
            if Problem.objects.filter(prob_id=prob_id,platform='C').exists():
                codechef(self.request.user.username,prob_id)
            if Problem.objects.filter(prob_id=prob_id,platform='S').exists():
                spoj(self.request.user.username,prob_id)
        return response.Response({'status' : "OK",'result' : 'ladder updated'},status = status.HTTP_200_OK)

class updateListView(generics.GenericAPIView):
    serializer_class = UpdateListSerializer

    def post(self,request,*args,**kwargs):
        list_slug = self.request.GET.get('slug')
        page = self.request.GET.get('page')
        if list_slug is None or list_slug == "" :
            return response.Response(data={'status' : 'FAILED','error' : 'No list provided'})
        curr_list = List.objects.get(slug=list_slug)
        cnt = int(curr_list.problem.all().count()/page_size)
        if curr_list.problem.all().count() % page_size != 0:
            cnt += 1
        if page is None or page == "":
            return response.Response(data={'status' : 'FAILED','error' :'No page provided'})
        if page > cnt:
            return response.Response(data={'status' : 'FAILED','error' :'Page out of bounds'})
        #set page size here and in the serializer list waala
        page_size = 6
        paginator = Paginator(curr_list.problem.all(),page_size)
        qs = paginator.page(page)  
        check = {'S' : set(),'U' : 0,'C' : set(),'F' : 0,'A' : 0}
        for prob in qs:
            platform = prob.platform
            if not Solved.objects.filter(user=self.request.user,problem__prob_id=prob.prob_id).exists():
                if platform == 'S' or platform == 'C':
                    check[platform].add(prob.prob_id)
                else:
                    check[platform] += 1
        print(check)
        if check['F'] > 0:
            cron_codeforces(self.request.user.username) 
        if check['U'] > 0:
            cron_uva(self.request.user.username)
        if check['A'] > 0:
            cron_atcoder(self.request.user.username)
        if len(check['S']) > 0:
            for item in check['S']:
                spoj(self.request.user.username,item)
        if len(check['C']) > 0:
            list1 = codechef_list(self.request.user.username)
            list2 = check['C']
            final = set((list1) & (list2))
            for ele in final:
                prob = Problem.objects.get(prob_id=ele,platform='C')
                user = self.request.user
                Solved.objects.create(user=user,problem=prob)
        return response.Response(data={'status' : 'OK','result' :'list updated'})


class UserlistGetView(generics.ListAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = GetUserlistSerializer
    
    def get_queryset(self):
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
        if prob_id is None or slug is None:
            return response.Response({"status" : 'FAILED','error' :"prob_id or slug or both not provided"},status=status.HTTP_400_BAD_REQUEST)
        if not List.objects.filter(slug = slug).exists():
            return response.Response({"status" : 'FAILED','error' :"List with the provided slug does not exist"},status=status.HTTP_400_BAD_REQUEST)
        if not Problem.objects.filter(prob_id = prob_id).exists():
            return response.Response({"status" : 'FAILED','error' :"Problem with the given prob_id does not exist"},status=status.HTTP_400_BAD_REQUEST)
        curr_list = List.objects.get(slug=slug)
        curr_prob = Problem.objects.get(prob_id=prob_id)
        if curr_list.problem.filter(prob_id=prob_id).exists():
            return response.Response({"status" : 'FAILED','error' :"Problem with the given prob_id already exists within the list"},status=status.HTTP_400_BAD_REQUEST)
        curr_list.problem.add(curr_prob)
        return response.Response({"status" : 'OK','result' :"Given problem has been added to the list"},status = status.HTTP_200_OK)


class EditUserlistView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthenticatedActivated]
    serializer_class = EditUserlistSerializer
    queryset = List.objects.all()
    lookup_field = 'slug'

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data

    def update(self,request,**kwargs):
        data = request.data
        if data.get('prob_id',None):
            for ele in data.get('prob_id',None):
                if not Problem.objects.filter(prob_id = ele).exists():
                    return response.Response({"status" : 'FAILED','error' :"Problem with the prob_id " + ele + " does not exist"},status=status.HTTP_400_BAD_REQUEST) 
                if not List.objects.filter(slug = data['slug']).exists():
                    return response.Response({"status" : 'FAILED','error' :"List with the provided slug does not exist"},status=status.HTTP_400_BAD_REQUEST)
                curr_prob = Problem.objects.get(prob_id=ele)
                curr_list = List.objects.get(slug=data['slug'])
                if not curr_list.problem.filter(prob_id=ele).exists():
                    return response.Response({"status" : 'FAILED','error' :"Problem with the given prob_id " + ele + " does not exists within the list"},status=status.HTTP_400_BAD_REQUEST) 
                curr_list.problem.remove(curr_prob)
        return super().update(request,**kwargs)