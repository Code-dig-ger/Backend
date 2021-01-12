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
from django.db.models import Q

from django.template.loader import render_to_string


def data(URL):
    return requests.get(URL).json()



class MentorAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GuruSerializer

    def get(self,request):
        return JsonResponse({'gurus':Profile.objects.get(owner=self.request.user).gurus.split(',')[1:-1]    })

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

        gym=request.GET.get('gym')
        divs = request.GET.get('divs')
        mentor=request.GET.get('mentor')

        #TODO get gurus from DB
        gurus = Profile.objects.get(owner=self.request.user).gurus.split(',')[1:-1]
 
        #TODO get user handle
        student = Profile.objects.get(owner=self.request.user).codeforces

        #fetch student data from api

        res=requests.get("https://codeforces.com/api/user.status?handle="+student)

        if res.status_code!=200:
            return JsonResponse({'status':'FAILED'}) 
        res=res.json()
        
        if res['status']!="OK":
            return JsonResponse({'status':'FAILED'}) 
        submissions_student = res["result"]
    
        #student submissions in set
        student_contests=set()
        for submission in submissions_student:
            if (submission['verdict']=='OK'):
                student_contests.add(submission["problem"]["contestId"])
        

        if mentor=='false':
            q = Q()
            for contestId in student_contests:
                q|=Q(contestId=contestId)
            contest_qs=contest.objects.exclude(q)

        else:
            guru_contests=set()
            for guru in gurus:

                res = requests.get("https://codeforces.com/api/user.status?handle="+guru)
                if res.status_code!=200:
                    return JsonResponse({'status':'FAILED'}) 
                res=res.json()
                if res['status']!="OK":
                    return JsonResponse({'status':'FAILED'})

                submissions_guru =  res['result']

                for submission in submissions_guru:
                    
                    if 'contestId' not in submission['problem']:
                        continue

                    if (submission['author']['participantType']!='PRACTICE') & (submission['verdict']=='OK'):
                        guru_contests.add(submission["problem"]["contestId"])
            
            #Select contest Ids which are not in student set
            contest_list=[]
            for contest_ in guru_contests:
                if contest_ not in student_contests:
                    contest_list.append(contest_)
            
            
            contest_qs = contest.objects.filter(contestId__in=contest_list)

        if gym == 'false':
            contest_qs=contest_qs.filter(Type='Regular')

        if divs!=None:
            divs = divs.split(',')
            q = Q()
            for div in divs:
                q|=Q(name__icontains=div)
                
            contest_qs = contest_qs.filter(q).order_by('?')[:20]
        context = { 'status':'OK', 'contest_qs':ContestSerializer(contest_qs,many=True).data }
        return JsonResponse( context )

class MentorProblemAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = GuruSerializer

    
    def get(self,request):
        
        #Mentors from Profile
        gurus = Profile.objects.get(owner=self.request.user).gurus.split()[1:-1]

        #User handle from Profile
        student = Profile.objects.get(owner=self.request.user).codeforces

       
        #fetch student submissions from api

        res = requests.get("https://codeforces.com/api/user.status?handle="+student)
        if res.status_code!=200:
            return JsonResponse({'status':'FAILED'}) 
        res=res.json()
        if res['status']!="OK":
            return JsonResponse({'status':'FAILED'})

        submissions_student = res["result"]

        student_solved_set = set()
        guru_solved_set = set()
        guru_solved_list = []

        
        for guru in gurus:

            res = requests.get("https://codeforces.com/api/user.status?handle="+guru)
            if res.status_code!=200:
                return JsonResponse({'status':'FAILED'}) 
            res=res.json()
            if res['status']!="OK":
                return JsonResponse({'status':'FAILED'})
            
            submissions_guru = res["result"]
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