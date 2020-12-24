import requests

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


