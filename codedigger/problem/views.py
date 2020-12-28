from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions,status

# Django Models Stuff
from .models import Problem
from user.models import Profile
from codeforces.models import contest ,user_contest_rank
from django.db.models import Q

# Serializer and Extra Utils Function
from .serializers import ProbSerializer , UpsolveContestSerializer , CCUpsolveContestSerializer,SolveProblemsSerializer
from .utils import codeforces_status , codechef_status
import json
from django.http import JsonResponse
from codeforces.views import MentorProblemAPIView



class SolveProblemsAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,generics.GenericAPIView
    ):

    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = SolveProblemsSerializer
    def post(self ,request):

        problems_list = []
        tags = request.data.get('tags').strip().split(' ')
        if request.data.get('mentors')==True:
            problems_list = MentorProblemAPIView.get(self,request)
            final_list=[]
            for problem in problems_list:
                intersection  = [tag for tag in tags if tag in problem['tags'] ]
                if len(intersection) !=0:
                    final_list.append(problem)

            return JsonResponse({'status':'OK' , 'problems_list':final_list  })
        else:
            problems_list = Problem.objects.all()
            problems_list = [ problem for problem in problems_list if problem['tags'] in tags ]
            return JsonResponse({'status':'OK' , 'problems_list':problems_list  })

        
class StatusAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = ProbSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = Problem.objects.all()
        prob = self.request.GET.get('prob_id')
        tags = self.request.GET.get('tags')
        if prob is not None:
            qs = qs.filter(prob_id__icontains = prob)
        if tags is not None:
            qs = qs.filter(tags__icontains = tags)
        return qs

SolvedInContest = None
Upsolved = None 
Wrong = None

class UpsolveContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticated]
    #authentication_classes = [SessionAuthentication]
    serializer_class = UpsolveContestSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):
        global SolvedInContest 
        global Upsolved 
        global Wrong
        handle = Profile.objects.get(owner =self.request.user).codeforces
        virtual = self.request.GET.get('virtual')
        RContest , VContest , SolvedInContest , Upsolved , Wrong = codeforces_status(handle)
        if virtual == 'true':
            RContest = RContest.union(VContest)
        c = contest.objects.filter(contestId__in = list(RContest))
        return c

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['wrong'] = Wrong
        data['solved'] = SolvedInContest
        data['upsolved'] = Upsolved
        return data

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

        if handle == "" :
            return Response({'status' : 'FAILED' , 'error' : 'You haven\'t Entered your Codechef Username in your Profile.. Update Now!' })

        Upsolved , SolvedInContest , Contest , ContestName = codechef_status(handle)

        #print(Contest)

        qs = Problem.objects.filter(Q(contest_id__in = list(Contest)) | Q(index__in = list(Contest)))

        data = {}
        data['contestName'] = ContestName
        data['solved'] = SolvedInContest
        data['upsolved'] = Upsolved

        return Response({'status' : 'OK'})

       
