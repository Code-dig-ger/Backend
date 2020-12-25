import re
import json
import requests
from bs4 import BeautifulSoup as bs4

def codeforces_status(handle) : 

	RContest = set()
	VContest = set()
	SolvedInContest = set()
	Upsolved = set()
	Wrong = set()
	
	url = "https://codeforces.com/api/user.status?handle="+handle
	res = requests.get(url)

	if res.status_code != 200:
		return (RContest , VContest , SolvedInContest , Upsolved , Wrong)

	data = res.json()

	if data['status'] != 'OK' : 
		return (RContest , VContest , SolvedInContest , Upsolved , Wrong)

	del res

	for submission in data['result']:
	    if 'contestId' in submission :
	        # to be sure this is a contest problem 
	        contestId = submission['contestId']
	        
	        if submission['author']['participantType'] == 'CONTESTANT' :
	            RContest.add(contestId)
	        elif submission['author']['participantType'] != 'PRACTICE'  :
	            VContest.add(contestId)
	            
	        if 'verdict' in submission :
	            # to be sure verdict is present 
	            if submission['verdict'] == 'OK' : 
	                if submission['author']['participantType'] != 'PRACTICE' :
	                    SolvedInContest.add(str(submission['problem']['contestId']) + submission['problem']['index'])
	                else :
	                    Upsolved.add(str(submission['problem']['contestId']) + submission['problem']['index'])

	for submission in data['result']:
	    if 'contestId' in submission :
	        if 'verdict' in submission :
	            # to be sure verdict is present 
	            prob_id = str(submission['problem']['contestId']) + submission['problem']['index']
	            if submission['verdict'] != 'OK' and prob_id not in SolvedInContest and prob_id not in Upsolved: 
	                Wrong.add(prob_id)

	return (RContest , VContest , SolvedInContest , Upsolved , Wrong)

def codechef_status(handle):

	Practice = set()
	SolvedInContest = set()
	Contest = set()
	ContestName = {}

	url = "https://www.codechef.com/users/" + handle

	res = requests.get(url)
	if res.status_code != 200 :
		return (Practice , SolvedInContest , Contest , ContestName)

	soup = bs4(res.content , 'html5lib')
	finding_rating = re.findall(r'var all_rating = .*;', str(soup))
	finds = len(finding_rating) == 1

	if finds :
		s = finding_rating[0].replace('var all_rating = ' , '').replace(';' , '')
		contest_details = json.loads(s)
		del s 
		del finding_rating

	Contest = set()
	ContestName = {}
	for contest in contest_details :
		Contest.add(contest['code'])
		ContestName[contest['code']] = contest['name']

	problems_solved = soup.find('section' , {'class' : 'rating-data-section problems-solved'})

	del soup

	if problems_solved.find('h5').text == 'Fully Solved (0)':
		return (Practice , SolvedInContest , Contest , ContestName)
	else :

		FullySolved = problems_solved.find('article')
		del problems_solved

		if FullySolved.find('p').find('strong').text == 'Practice:' :
			Practice = {x.text for x in FullySolved.find('p').findAll('a')}
			SolvedInContest = set()
			for y in FullySolved.findAll('p')[1:] :
				for x in y.findAll('a') :
					SolvedInContest.add(x.text)
		else :
			SolvedInContest = {x.text for x in problems_solved.find('article').findAll('a')}

	return (Practice , SolvedInContest , Contest , ContestName)

