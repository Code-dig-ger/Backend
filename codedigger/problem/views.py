from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions,status

# Django Models Stuff
from .models import Problem , atcoder_contest
from user.models import Profile
from codeforces.models import contest ,user_contest_rank
from django.db.models import Q

# Serializer and Extra Utils Function

from .serializers import ProbSerializer , UpsolveContestSerializer , CCUpsolveContestSerializer , AtcoderUpsolveContestSerializer,SolveProblemsSerializer
from .utils import codeforces_status , codechef_status , atcoder_status
import json
from django.http import JsonResponse
from codeforces.views import MentorProblemAPIView
import random


class SolveProblemsAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,generics.GenericAPIView
    ):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SolveProblemsSerializer
    def get(self ,request):

        tags = request.GET.get('tags')
        platforms = request.GET.get('platform')
        difficulty = request.GET.get('difficulty')
        range_l = request.GET.get('range_l')
        range_r = request.GET.get('range_r')
        searches = request.GET.get('search')
        mentors=request.GET.get('mentor')
        
        if request.user.is_authenticated : 
            if mentors=='true':
                problems_list = MentorProblemAPIView.get(self,request).data['result']
                problem_qs = Problem.objects.filter( prob_id__in = problems_list )
            else :
                problems_list = MentorProblemAPIView.get(self,request).data['result']
                q = Q()
                for prob_id in problems_list:
                    q|=Q(prob_id=prob_id)
                problem_qs = Problem.objects.exclude(q)
        else:
            problem_qs = Problem.objects.all()

        if platforms is not None:
            platforms=platforms.split(',')
            problem_qs = problem_qs.filter( platform__in=platforms)

        if difficulty is not None:
            difficulty=difficulty.split(',')
            problem_qs = problem_qs.filter( difficulty__in = difficulty )

        if range_l is not None:
            problem_qs = problem_qs.filter(rating__gt=int(range_l) )
        
        if range_r is not None:
            problem_qs = problem_qs.filter(rating__lt=int(range_r))

        if searches is not None:
            searches=searches.split(',')
            for search in searches:
                q = Q()
                q|=Q(  name__icontains = search)
                q|=Q(  prob_id__icontains = search)
                q|=Q(  url__icontains = search)
                q|=Q(  tags__icontains = search)
                q|=Q(  contest_id__icontains = search )

            problem_qs = problem_qs.filter(q)

        if tags is not None:
            tags=tags.split(',')
            q = Q()
            for tag in tags:
                q|=Q(tags__icontains=tag) 
            problem_qs = problem_qs.filter(q)

        problem_qs = problem_qs.order_by('?')[:20]
        return JsonResponse({'status':'OK' , 'problems_list':ProbSerializer(problem_qs, many = True).data  })

class UpsolveContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticated]
    #authentication_classes = [SessionAuthentication]
    serializer_class = UpsolveContestSerializer
    #passed_id = None 

    #running queries and stuff
    def get(self , request):
        handle = Profile.objects.get(owner = self.request.user).codeforces
        if handle == "" or handle == None :
            return Response({'status' : 'FAILED' , 'error' : 'Please activate your account once by putting your name and codeforces handle..'})
        virtual = request.GET.get('virtual')
        page = request.GET.get('page')
        path = request.build_absolute_uri('/problems/upsolve/codeforces')
        if virtual != None:
            path = path + '?virtual='+virtual+';'
        else:
            path = path + '?'
        if page == None:
            page = 1
        elif page.isdigit():
            page = int(page)
        else: 
            return Response({'status' : 'FAILED' , 'error' : 'Page must be an integer.'})
        RContest , VContest , SolvedInContest , Upsolved , Wrong = codeforces_status(handle)
        data = {
            'wrong'  : Wrong , 
            'solved' : SolvedInContest , 
            'upsolved' : Upsolved , 
        }
        if virtual == 'true':
            RContest = RContest.union(VContest)
        RContest = list(RContest)
        total = len(RContest)
        NumPage = (len(RContest)-1)//10 + 1  # Number of page
        if NumPage == 0 :
            return Response({'status' : 'OK' , 'result' : []})
        if page > NumPage : 
            return Response({'status' : 'FAILED' , 'error' : 'Page Out of Bound'})
        if page == NumPage :
            Next = None
        else :
            Next = path + 'page='+str(page+1)
        if page == 1:
            Prev = None
        else :
            Prev = path + 'page='+str(page-1)
        RContest = RContest[10*(page-1) : 10*page]    
        c = contest.objects.filter(contestId__in = RContest)
        return Response({
            'status' : 'OK' , 
            'result' : UpsolveContestSerializer(c, many =True, context = data).data, 
            'links' : {
                'first' : path + 'page=1',
                'last' : path + 'page='+str(NumPage),
                'prev' : Prev,
                'next' : Next
            },
            'meta' : {
                'current_page' : page,
                'from' : (page-1)*10 + 1,
                'last_page' : NumPage,
                'path' : request.build_absolute_uri('/problems/upsolve/codeforces'),
                'per_page' : 10,
                'to' : page*10,
                'total' : total
            }
        })

class CCUpsolveContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticated]
    #authentication_classes = [SessionAuthentication]
    serializer_class = CCUpsolveContestSerializer
    #passed_id = None 

    def get(self , request):

        handle = Profile.objects.get(owner =self.request.user).codechef

        if handle == "" or handle == None:
            return Response({'status' : 'FAILED' , 'error' : 'You haven\'t Entered your Codechef Username in your Profile.. Update Now!' })

        page = request.GET.get('page')
        path = request.build_absolute_uri('/problems/upsolve/codechef')+'?'

        if page == None:
            page = 1
        elif page.isdigit():
            page = int(page)
        else: 
            return Response({'status' : 'FAILED' , 'error' : 'Page must be an integer.'})

        Upsolved , SolvedInContest , Contest , ContestName = codechef_status(handle)

        total = len(Contest)
        NumPage = (len(Contest)-1)//10 + 1  # Number of page
        if NumPage == 0 :
            return Response({'status' : 'OK' , 'result' : []})
        if page > NumPage : 
            return Response({'status' : 'FAILED' , 'error' : 'Page Out of Bound'})
        if page == NumPage :
            Next = None
        else :
            Next = path + 'page='+str(page+1)
        if page == 1:
            Prev = None
        else :
            Prev = path + 'page='+str(page-1)
        
        Contest = list(Contest)
        Contest = Contest[10*(page-1) : 10*page]    

        data = {
            'solved'  : SolvedInContest,
            'upsolved' : Upsolved
        }

        user_contest_details = []

        for contest in Contest :
            qs = Problem.objects.filter(Q(contest_id = contest) | Q(index = contest))
            if qs.count() > 0 :
                user_contest_details.append({
                    'contestId' : contest,
                    'name' :  ContestName[contest],
                    'problems' :CCUpsolveContestSerializer(qs , many =True , context = data).data 
                })

        return Response({
            'status' : 'OK' , 
            'result' : user_contest_details ,
            'links' : {
                'first' : path + 'page=1',
                'last' : path + 'page='+str(NumPage),
                'prev' : Prev,
                'next' : Next
            },
            'meta' : {
                'current_page' : page,
                'from' : (page-1)*10 + 1,
                'last_page' : NumPage,
                'path' : request.build_absolute_uri('/problems/upsolve/codechef'),
                'per_page' : 10,
                'to' : page*10,
                'total' : total
            }
        })

class ATUpsolveContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticated]
    #authentication_classes = [SessionAuthentication]
    serializer_class = AtcoderUpsolveContestSerializer
    #passed_id = None 

    def get(self , request):

        handle = Profile.objects.get(owner =self.request.user).atcoder

        if handle == "" or handle == None:
            return Response({'status' : 'FAILED' , 'error' : 'You haven\'t Entered your Atcoder Handle in your Profile.. Update Now!' })
        practice = request.GET.get('practice')
        page = request.GET.get('page')
        path = request.build_absolute_uri('/problems/upsolve/atcoder')
        if practice != None:
            path = path + '?practice='+practice+';'
        else:
            path = path + '?'
        if page == None:
            page = 1
        elif page.isdigit():
            page = int(page)
        else: 
            return Response({'status' : 'FAILED' , 'error' : 'Page must be an integer.'})
        
        contests_details , all_contest , solved , wrong = atcoder_status(handle)
        if practice == 'true':
            contests_details = contests_details.union(all_contest)

        contests_details = list(contests_details)
        total = len(contests_details)
        NumPage = (len(contests_details)-1)//10 + 1  # Number of page
        if NumPage == 0 :
            return Response({'status' : 'OK' , 'result' : []})
        if page > NumPage : 
            return Response({'status' : 'FAILED' , 'error' : 'Page Out of Bound'})
        if page == NumPage :
            Next = None
        else :
            Next = path + 'page='+str(page+1)
        if page == 1:
            Prev = None
        else :
            Prev = path + 'page='+str(page-1)
        contests_details = contests_details[10*(page-1) : 10*page] 

        data = {
            'solved'  : solved,
            'wrong' : wrong
        }

        qs = atcoder_contest.objects.filter(contestId__in = contests_details)

        return Response({
            'status' : 'OK' , 
            'result' : AtcoderUpsolveContestSerializer(qs , many = True , context = data).data ,
            'links' : {
                'first' : path + 'page=1',
                'last' : path + 'page='+str(NumPage),
                'prev' : Prev,
                'next' : Next
            },
            'meta' : {
                'current_page' : page,
                'from' : (page-1)*10 + 1,
                'last_page' : NumPage,
                'path' : request.build_absolute_uri('/problems/upsolve/atcoder'),
                'per_page' : 10,
                'to' : page*10,
                'total' : total
            }
        })