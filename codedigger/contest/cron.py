# Cron Job -
# Problem Assign -- Contest with isProblem False -- Assign Problem 
# Result Assign -- Contest with isResult False 
# contest end -- (startTime + duration) <= time.now 

#Email
from django.core.mail import send_mail	
from codedigger.settings import EMAIL_HOST_USER

## Short Code Contest 
from .utils import login, clean, penalty
from .models import CodeforcesContest, CodeforcesContestSubmission, CodeforcesContestParticipation
import requests, random, re
from codeforces.cron import save_user
from codeforces.models import user as CodeforcesUser
from bs4 import BeautifulSoup as bs

def update_penalty(contest, cookie) :
	contestId = contest.contestId
	groupId = contest.groupId
	page = 0
	prevHandle = None
	while(page < 100):
		page+=1
		url = "https://codeforces.com/group/"+groupId+"/contest/"+str(contestId)+"/standings/page/"+str(page)
		res = requests.get(url , headers = {'Cookie' : cookie})
		soup = bs(res.content,features="html5lib")
		participants = soup.find('table' , {'class' :'standings'}).findAll('tr')
		NProblems = len(participants[0].findAll('th'))-4
		isBreak = False
		isFirst = True

		for participant in participants[1:-1] :
			column = participant.findAll('td')
			user_handle = clean(column[1].find('a').text)
			if isFirst:
				if user_handle == prevHandle:
					isBreak = True
					break
				else :
					prevHandle = user_handle
					isFirst = False
			contest_user,created = CodeforcesUser.objects.get_or_create(handle = user_handle)
			if created : 
				url = "https://codeforces.com/api/user.info?handles="+user_handle
				res = requests.get(url)
				if res.status_code == 200:
					data = res.json()
					if data['status'] == 'OK':
						save_user(contest_user , data['result'][0])

			contest_participant,created = CodeforcesContestParticipation.objects.get_or_create(
				contest=contest,
				user=contest_user,
				participantId=participant['participantid'],
				defaults={
					'isOfficial' : clean(column[0].text) != '',
					'isVirtual' : column[1].find('sup') != None
				})

			for i in range(NProblems):

				sub = CodeforcesContestSubmission.objects.filter(participant=contest_participant, problemIndex = i)

				newSub = CodeforcesContestSubmission(participant=contest_participant, problemIndex = i)

				if column[4+i].find('span' , {'class' : 'cell-accepted'})!=None and column[4+i]['title'][:3]=='GNU':
					subId = participant.findAll('td')[4+i]['acceptedsubmissionid']

					if sub.exists() and str(sub[0].submissionId) == subId :
						continue

					if sub.exists() :
						sub[0].isSolved = True
						sub[0].submissionId = subId
						sub[0].lang = column[4+i]['title']
						sub[0].penalty = penalty(cookie, contestId, subId, groupId)
						sub[0].save()
					else :
						newSub.isSolved = True
						newSub.submissionId = subId
						newSub.lang = column[4+i]['title']
						newSub.penalty = penalty(cookie, contestId, subId, groupId)
						newSub.save()
				else :
					newSub.isSolved = False
					if not sub.exists() :
						newSub.save()

		if isBreak:
			break

def update_codeforces_short_code_contests() : 
	cookie = login()
	codeforcescontest = CodeforcesContest.objects.filter(Type = "Short Code")
	for contest in codeforcescontest : 
		update_penalty(contest, cookie)