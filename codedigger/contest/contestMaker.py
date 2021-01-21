import requests
from .models import Contest,ContestProblem,ContestParticipation
from user.models import Profile
from problem.models import Problem

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


def makeContest(contest):
	
	nProblems = contest.numberOfProblem
	platforms = list(contest.platform) # TODO Till now we are using only codeforces 
	tags = contest.tag.split(',')[1:-1]
	rating = contest.rating # TODO We will take count this too later
	difficulty = contest.difficulty 
	isMentorOn = contest.isMentorOn

	participants = ContestParticipation.objects.filter(contest = contest).values_list('user', flat=True)
	participants_codeforces =  list(Profile.objects.filter(owner__in = participants).values_list('codeforces' ,flat=True))
	participants_solved = get_participant_problem(participants_codeforces)

	problems = Problem.objects.filter(platform = 'F') # TODO all platform 
	
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

	# TODO more filter on problems e.g. by TAG

	# TODO Assuming Div2 only 

	div = 'div2'

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

	contest.isProblem = True
	contest.save()
	return

