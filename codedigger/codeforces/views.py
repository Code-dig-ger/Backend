from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions 

from .models import user,country,organization,contest
from .serializers import UserSerializer,CountrySerializer,OrganizationSerializer,ContestSerializer
from user.serializers import GuruSerializer
from problem.serializers import ProbSerializer
import json,requests
from django.http import JsonResponse
from user.models import Profile
from .cron import ratingChangeReminder

def data(URL):
    return requests.get(URL).json()



class MentorAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GuruSerializer

    def get(self,request):
        return JsonResponse({'gurus':Profile.objects.get(owner=self.request.user).gurus})

    def put(self,request):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.add(validated_data=request.data,instance = Profile.objects.get(owner=self.request.user) )

        return Response({'success': True, 'message': 'Guru List Updated'})
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.delete(instance = Profile.objects.get(owner=self.request.user), data=request.data)

        return Response({'success': True, 'message': 'Guru List Updated'})



class MentorContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = GuruSerializer

    
    def get(self,request):
        #TODO get gurus from DB
        gurus = [ 'Ashishgup','coder_pulkit_c']

        #TODO get user handle
        student = "Shashank_Chugh"

        #fetch student data from api
        submissions_student = data("https://codeforces.com/api/user.status?handle="+student)["result"]
        
        guru_contests={}
        student_contests=set()

        #student submissions in set
        for submission in submissions_student:
            if (submission['author']['participantType']!='PRACTICE') &  (submission["problem"]["contestId"] <100000) & (submission['verdict']=='OK'):
                student_contests.add(submission["problem"]["contestId"])

        #iterate over gurus , to get relevant contestIds 
        for guru in gurus:
            fetched_data = data("https://codeforces.com/api/user.status?handle="+guru)
        
            submissions_guru = fetched_data["result"]
            for submission in submissions_guru:
                if 'contestId' not in submission['problem']:
                    continue
                if (submission['author']['participantType']!='PRACTICE') &  (submission["problem"]["contestId"] <100000) & (submission['verdict']=='OK'):
                  
                    if (str(submission["problem"]["contestId"]) not in guru_contests)   :
                        guru_contests[str(submission["problem"]["contestId"])] =1
                    else:
                        guru_contests[str(submission["problem"]["contestId"])]+=1
        
        guru_contests = sorted(guru_contests.items(), key=lambda x: x[1], reverse=True)
        print(guru_contests)
        contest_list=[]
        for contest in guru_contests:
            contest_list.append(contest[0])


        context = { 'status':'OK' , 'contest_list':contest_list}
        return JsonResponse( context )

class MentorProblemAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = GuruSerializer

    
    def get(self,request):
        
        #TODO get gurus from DB
        gurus = ['coder_pulkit_c']

        #TODO get user handle
        student = "Shashank_Chugh"

       
        #fetch student submissions from api
        submissions_student = data("https://codeforces.com/api/user.status?handle="+student)["result"]

        student_solved_set = set()
        guru_solved_set = set()
        guru_solved_list = []


        #TODO filter using tags

        for guru in gurus:
            fetched_data =data("https://codeforces.com/api/user.status?handle="+guru)
            if fetched_data['status']!='OK':
                return HttpResponse("ERROR")

            submissions_guru = fetched_data["result"]
            for submission in submissions_guru:
                if str(submission["problem"]['contestId'])+submission["problem"]['index'] in guru_solved_set:
                    continue 
                elif submission['verdict']=='OK':
                    guru_solved_set.add(str(submission["problem"]['contestId'])+submission["problem"]['index'])
                    guru_solved_list.append(submission["problem"])

        for submission in submissions_student:
            if submission['verdict']=='OK':
                student_solved_set.add(str(submission["problem"]['contestId'])+submission["problem"]['index'])
        
        problems_data=[]
        sno=0
        for problem in guru_solved_list:
            
            if str(problem["contestId"])+problem['index'] not in student_solved_set:
                # problems_data.append(str(problem["contestId"])+"/problem/"+problem['index'] ) 
                # problems_name.append(problem['name'])  
                # print("https://codeforces.com/contest/"+str(problem["contestId"])+"/problem/"+problem['index'] + ' RED' )
                sno+=1
                link = "https://codeforces.com/contest/"+str(problem["contestId"])+"/problem/"+problem['index']
                rating  = "" 
                if 'rating' in problem:
                    rating = problem["rating"]
                problems_data.append(  { 'index':problem['index']  , 'contestId':problem['contestId']  }           )

        return Response({'status' : 'OK' , 'result' : problems_data})

from problem.models import Problem
import json


class UsersAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = UserSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = user.objects.all()
        handle = self.request.GET.get('handle')
        if handle is not None:
            qs = qs.filter(handle = handle)
        return qs

class ProblemsAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = ProbSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = Problem.objects.all().filter(platform = 'F')
        tags = self.request.GET.get('tags')
        if tags is not None:
            qs = qs.filter(tags_icontains = tags)
        return qs

class CountryAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = CountrySerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = country.objects.all()
        name = self.request.GET.get('name')
        if name is not None:
            qs = qs.filter(name = name)
        return qs

class OrganizationAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = OrganizationSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = organization.objects.all()
        name = self.request.GET.get('name')
        if name is not None:
            qs = qs.filter(name = name)
        return qs


class ContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = ContestSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = contest.objects.all()
        contestId = self.request.GET.get('contestId')
        if contestId is not None:
            qs = qs.filter(contestId = contestId)
        return qs

    
def testing(request):

    ratingChangeReminder()
    return JsonResponse({'data':1})