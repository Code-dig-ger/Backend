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



class SolveProblemsAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,generics.GenericAPIView
    ):

    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = SolveProblemsSerializer
    def post(self ,request):

        tags = request.data.get('tags')
        if request.data.get('mentors')==True:
            problems_list = MentorProblemAPIView.get(self,request).data
            final_list=[]
            #print(problems_list)
            for problem in problems_list['result']:
                qs = Problem.objects.filter(contest_id=problem['contestId'] , index = problem['index'] )
                problem_added=qs.filter(tags__icontains=tags)
                if len(problem_added)!=0:
                    final_list.append(problem_added[0])

            # Logic -- If less than 20 problem send them 
            # Else Only 20  
            return JsonResponse({'status':'OK' , 'problems_list':ProbSerializer(final_list, many = True).data})
        else:
            # Logic -- If less than 20 problem send them 
            # Else Only 20 
            # Shuffle   
            problems_list = Problem.objects.filter(tags__icontains=tags).order_by('?')
            return JsonResponse({'status':'OK' , 'problems_list':ProbSerializer(problems_list, many = True).data  })

        
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

        RContest , VContest , SolvedInContest , Upsolved , Wrong = codeforces_status(handle)

        data = {
            'wrong'  : Wrong , 
            'solved' : SolvedInContest , 
            'upsolved' : Upsolved , 
        }

        if virtual == 'true':
            RContest = RContest.union(VContest)

        c = contest.objects.filter(contestId__in = list(RContest))

        return Response({'status' : 'OK' , 'result' : UpsolveContestSerializer(c, many =True, context = data).data})


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

        Upsolved , SolvedInContest , Contest , ContestName = codechef_status(handle)

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

        return Response({'status' : 'OK' , 'result' : user_contest_details})

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

        contests_details , all_contest , solved , wrong = atcoder_status(handle)

        practice = request.GET.get('practice')
        
        if practice == 'true':
            contests_details = contests_details.union(all_contest)

        data = {
            'solved'  : solved,
            'wrong' : wrong
        }

        qs = atcoder_contest.objects.filter(contestId__in = contests_details)

        return Response({'status' : 'OK' , 'result' : AtcoderUpsolveContestSerializer(qs , many = True , context = data).data})