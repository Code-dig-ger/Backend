from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions  


from codeforces.models import user,country,organization,contest
from codeforces.serializers import UserSerializer,CountrySerializer,OrganizationSerializer,ContestSerializer
from user.serializers import GuruSerializer
from problem.serializers import ProbSerializer
import json,requests
from django.http import JsonResponse
from user.models import Profile
from django.db.models import Q

from django.template.loader import render_to_string

from rest_framework import generics,status,permissions,views
from user.permissions import *

# Create your views here.

class ContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [AuthenticatedActivated]
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
            return Response({'status' : 'FAILED' , 'error' : 'Codeforces API not working'},status = status.HTTP_400_BAD_REQUEST)
        res=res.json()
        
        if res['status']!="OK":
            return Response({'status' : 'FAILED' , 'error' : 'Codeforces API not working'},status = status.HTTP_400_BAD_REQUEST)
        submissions_student = res["result"]
    
        #student submissions in set
        student_contests=set()
        for submission in submissions_student:
            if (submission['verdict']=='OK'):
                student_contests.add(submission["problem"]["contestId"])
        
        if mentor=='true':
            guru_contests=set()
            for guru in gurus:

                res = requests.get("https://codeforces.com/api/user.status?handle="+guru)
                if res.status_code!=200:
                    return Response({'status' : 'FAILED' , 'error' : 'Codeforces API not working'},status = status.HTTP_400_BAD_REQUEST)
                res=res.json()
                if res['status']!="OK":
                    return Response({'status' : 'FAILED' , 'error' : 'Codeforces API not working'},status = status.HTTP_400_BAD_REQUEST)

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
        else:
            q = Q()
            for contestId in student_contests:
                q|=Q(contestId=contestId)
            contest_qs=contest.objects.exclude(q)

        if gym != 'true':
            contest_qs=contest_qs.filter(Type='R')

        if divs!=None:
            divs = divs.split(',')
            q = Q()
            for div in divs:
                q|=Q(name__icontains=div)
                
            contest_qs = contest_qs.filter(q)

        contest_qs = contest_qs.order_by('?')[:20]
        context = { 'status':'OK', 'result':ContestSerializer(contest_qs,many=True).data }
        return JsonResponse( context )
