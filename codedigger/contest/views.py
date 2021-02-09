from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions  


from codeforces.models import user,country,organization,contest
from codeforces.serializers import UserSerializer,CountrySerializer,OrganizationSerializer,ContestSerializer
from .models import *
from user.serializers import GuruSerializer
from problem.serializers import ProbSerializer
import json,requests
from django.http import JsonResponse
from user.models import Profile
from django.db.models import Q

from django.template.loader import render_to_string


from rest_framework import generics,status,permissions,views
from user.permissions import *

from .contestMaker import makeContest
from .resultMaker import prepareResult
import requests
from .models import Contest,ContestProblem,ContestParticipation
from user.models import Profile
from problem.models import Problem

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
		timeline =request.GET.get('timeline')

		gurus = Profile.objects.get(owner=self.request.user).gurus.split(',')[1:-1]
		students = Profile.objects.get(owner=self.request.user).codeforces
		#TODO convert to list

		#fetch student data from api
		student_contests=set()
		for student in students:
			res=requests.get("https://codeforces.com/api/user.status?handle="+student)
			if res.status_code!=200:
				return Response({'status' : 'FAILED' , 'error' : 'Codeforces API not working'},status = status.HTTP_400_BAD_REQUEST)
			res=res.json()
			if res['status']!="OK":
				return Response({'status' : 'FAILED' , 'error' : 'Codeforces API not working'},status = status.HTTP_400_BAD_REQUEST)
			submissions_student = res["result"]
		    #student submissions in set
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

		if timeline!=None:
			time = current_time - timeline*month_time
			contest_qs = contest_qs.filter(startTime__gt>time)

		contest_qs = contest_qs.order_by('?')[:20]
		context = { 'status':'OK', 'result':ContestSerializer(contest_qs,many=True).data }

		return JsonResponse( context )



def testing(request):

    contest = Contest.objects.all()[0]

    prepareResult(contest)

    return JsonResponse({'status' :  'OK'})



problem_rating = {

	'div1' : [ (1600,1900), (1900,2100), (2100,2300), (2300,2400), (2400,2600),
		(2600,2800), (2800,3000), (3000,3200), (3200,3400), (3400,3600) ],
	'div2' : [ (800,1000), (1000,1200), (1200,1600), (1600,1900),  (1900,2100), 
		(2100,2300), (2300,2400), (2400,2600), (2600,2800), (2800,3000) ],
	'div3' : [ (800,1000), (1000,1200), (1200,1400), (1400,1500), (1500,1600), 
		(1600,1900), (1900,2100), (2100,2300), (2300,2400), (2400,2600) ],
	'div4' : [ (800,900),  (900,1100), (1100,1200), (1200,1400), (1400,1500), 
		(1500,1600), (1600,1900), (1900,2100), (2100,2300), (2300,2400) ]
}

# this will return a list of problem according to the contest
# assign also 
# isProblem = true





def get_mentor_problems(mentor_codeforces):
	mentor_solved = set()
	
	for mentor in mentor_codeforces:
		res = requests.get("https://codeforces.com/api/user.status?handle="+mentor)
	
		if res.status_code!=200:
			return mentor_solved
	
		res=res.json()
	
		if res['status']!="OK":
			return mentor_solved
	
		for submission in res["result"]:
			if 'contestId' in submission['problem'] : 
				if submission['verdict']=='OK':
					mentor_solved.add(str(submission["problem"]['contestId'])+submission["problem"]['index'])
	
	return mentor_solved





def get_participant_problem(participants_codeforces):
	participants_solved = set() 
	
	for participants in participants_codeforces:
		res = requests.get("https://codeforces.com/api/user.status?handle="+participants)
	
		if res.status_code!=200:
			return participants_solved
	
		res=res.json()
	
		if res['status']!="OK":
			return participants_solved
	
		for submission in res["result"]:
			if 'contestId' in submission['problem'] : 
				participants_solved.add(str(submission["problem"]['contestId'])+submission["problem"]['index'])	
	
	return participants_solved





def makeContest( contest ):
	
	nProblems = request.POST.get('nProblems')
	platforms = request.POST.get('platforms') # TODO Till now  we are using only codeforces 
	tags = request.POST.get('tags')
	rating = request.POST.get('rating') # TODO We will take  count this too later
	difficulty = request.POST.get('difficulty')
	isMentorOn = request.POST.get('isMentorOn')
	isGym = request.POST.get('isGym') #TODO if false -> remove problems with -> platform='F' and len(contestId)>=6


	participants = ContestParticipation.objects.filter(contest = contest).values_list('user', flat=True)
	participants_codeforces =  list(Profile.objects.filter(owner__in = participants).values_list('codeforces' ,flat=True))
	participants_solved = get_participant_problem(participants_codeforces)

	problems = Problem.objects.filter(platform = 'F') # TODO all  platform 
	
	if isMentorOn :
		mentor_codeforces = Profile.objects.get(owner = contest.owner).gurus.split(',')[1:-1]
		mentor_solved = get_mentor_problems(mentor_codeforces)
		for ps in participants_solved :
			if ps in mentor_solved : 
				mentor_solved.remove(ps)

	
	if isMentorOn and len(mentor_solved) > 10:
		problems = problems.filter(prob_id__in = mentor_solved)
	else: 
		problems = problems.exclude(prob_id__in = participants_solved)

	if tags is not None:
		tags=tags.split(',')
		q = Q()    
		for tag in tags:
			q|=Q(tags__icontains=tag) 
			problems = problems.filter(q)

	# TODO more filter on problems  e.g. by TAG

	# TODO Assuming  Div2 only 

	div = difficulty

	nProblems = min(nProblems , problems.count())
	
	for i in range(0,nProblems):

		l,r = problem_rating[div][i]
		newProblem = ContestProblem()
		newProblem.contest = contest


		while not problems.filter(rating__gte = l , rating__lt = r).exists() : 
			l -= 100 
			r += 100
			if l < 0:
				break

		if problems.filter(rating__gte = l , rating__lt = r).exists() :
			newProblem.problem = problems.filter(rating__gte = l , rating__lt = r).order_by('?')[0]
			newProblem.index = i
			newProblem.save()


	contest.isProblem =  True
	contest.save()
	return

