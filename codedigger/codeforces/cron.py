import json
import requests

from django.db import connection
from problem.models import Problem 

from django.core.mail import send_mail	
from codedigger.settings import EMAIL_HOST_USER

from django.core.exceptions import ObjectDoesNotExist
from .models import organization , country , user , contest , user_contest_rank , organization_contest_participation, country_contest_participation


def rating_to_difficulty(rating):
	if rating <= 1100 : 
		return 'B'
	elif rating <= 1500:
		return 'E'
	elif rating <= 1800:
		return 'M'
	elif rating <= 2100:
		return 'H'
	elif rating <= 2600:
		return 'S'
	else :
		return 'C'

def alter_tables():	
	cursor = connection.cursor()
	cursor.execute('ALTER TABLE codeforces_organization CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci')
	cursor.execute('ALTER TABLE codeforces_user CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci')
	cursor.execute('ALTER TABLE codeforces_country CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci')
	cursor.execute('ALTER TABLE codeforces_contest CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci')
	cursor.execute('ALTER TABLE problem_problem CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci')
	cursor.execute('ALTER TABLE problem_atcoder_contest CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci')
	return


def codeforces_update_users():
	url = "https://codeforces.com/api/user.ratedList"
	res = requests.get(url)
	data= res.json()

	if(data["status"] != 'OK') :
		return 

	rank = 0
	organization.objects.all().update(current = 0)
	country.objects.all().update(current = 0)

	for codeforces_user in data["result"]:

		newUser,created = user.objects.get_or_create(handle = codeforces_user['handle'])
		name = ""
		if 'firstName' in codeforces_user:
			name += codeforces_user['firstName']
			name += " "
		if 'lastName' in codeforces_user:
			name += codeforces_user['lastName']

		if len(name) > 100 : 
			name = name[:100]

		newUser.name = name		
		newUser.rating = codeforces_user['rating']
		newUser.maxRating = codeforces_user['maxRating']
		newUser.rank = codeforces_user['rank']
		newUser.maxRank  = codeforces_user['maxRank']
		rank+=1
		newUser.worldRank = rank
		newUser.photoUrl = codeforces_user['titlePhoto'][2:]

		if 'country' in codeforces_user :

			obj, created = country.objects.get_or_create(
				name=  codeforces_user['country'] ,
				defaults={
					'current': '0',
					'total' : '0'
				}
			)

			obj.current = str(int(obj.current) + 1)
			if int(obj.current) > int(obj.total) :
				obj.total = obj.current
			obj.save()
			newUser.country = obj
			newUser.countryRank = obj.current

		if 'organization' in codeforces_user :

			obj, created = organization.objects.get_or_create(
				name=  codeforces_user['organization'] ,
				defaults={
					'current': '0',
					'total' : '0'
				}
			)

			obj.current = str(int(obj.current) + 1)
			if int(obj.current) > int(obj.total) :
				obj.total = obj.current
			obj.save()
			newUser.organization = obj
			newUser.organizationRank = obj.current

		newUser.save()
	return 

def codeforces_update_problems():
	# check whether we have updated the problems of a particular contest , 
	# if no , update the problems , else not .. 
	url = "https://codeforces.com/api/contest.list"
	res = requests.get(url)
	data = res.json()

	if(data["status"] != 'OK') :
		return 

	for codeforces_contest in data['result'] : 

		url = "https://codeforces.com/api/contest.standings?contestId=" + str(codeforces_contest['id']) + "&from=1&count=1"
		res = requests.get(url)
		data= res.json()

		if(data["status"] != 'OK') :
			continue 

		new_contest = contest()
		if 'startTimeSeconds' in codeforces_contest:
			new_contest.startTime = codeforces_contest['startTimeSeconds']

		new_contest.Type = 'R'
		new_contest.contestId = codeforces_contest['id']
		new_contest.name = codeforces_contest['name']
		new_contest.duration = codeforces_contest['durationSeconds']

		if len(contest.objects.filter(contestId=codeforces_contest['id'])) == 0: 
			new_contest.save()

		for contest_problem in data['result']['problems']:
			new_problem = Problem()
			new_problem.name = contest_problem['name']
			new_problem.contest_id = contest_problem['contestId']
			new_problem.prob_id = str(contest_problem['contestId']) + contest_problem['index']
			new_problem.url = "https://codeforces.com/contest/"+ str(contest_problem['contestId'])+"/problem/"+contest_problem['index']
			new_problem.platform = 'F'  
			new_problem.index = contest_problem['index']
			new_problem.tags = contest_problem['tags']
			if 'rating' in contest_problem : 
				new_problem.rating = contest_problem['rating']
				new_problem.difficulty = rating_to_difficulty(int(contest_problem['rating']))

			if len(Problem.objects.filter(prob_id = str(contest_problem['contestId']) + contest_problem['index'])) == 0: 
				new_problem.save()
	
	url = "https://codeforces.com/api/contest.list?gym=true"
	res = requests.get(url)
	data = res.json()

	if(data["status"] != 'OK') :
		return 

	for codeforces_contest in data['result'] : 

		url = "https://codeforces.com/api/contest.standings?contestId=" + str(codeforces_contest['id']) + "&from=1&count=1"
		res = requests.get(url)
		data= res.json()

		if(data["status"] != 'OK') :
			continue 

		new_contest = contest()
		if 'startTimeSeconds' in codeforces_contest:
			new_contest.startTime = codeforces_contest['startTimeSeconds']

		new_contest.Type = 'R'
		new_contest.contestId = codeforces_contest['id']
		new_contest.name = codeforces_contest['name']
		new_contest.duration = codeforces_contest['durationSeconds']

		if len(contest.objects.filter(contestId=codeforces_contest['id'])) == 0: 
			new_contest.save()

		for contest_problem in data['result']['problems']:
			new_problem = Problem()
			new_problem.name = contest_problem['name']
			new_problem.contest_id = contest_problem['contestId']
			new_problem.prob_id = str(contest_problem['contestId']) + contest_problem['index']
			new_problem.url = "https://codeforces.com/gym/"+ str(contest_problem['contestId'])+"/problem/"+contest_problem['index']
			new_problem.platform = 'F'  
			new_problem.index = contest_problem['index']
			new_problem.tags = contest_problem['tags']
			if 'rating' in contest_problem : 
				new_problem.rating = contest_problem['rating']
				new_problem.difficulty = rating_to_difficulty(int(contest_problem['rating']))

			if len(Problem.objects.filter(prob_id = str(contest_problem['contestId']) + contest_problem['index'])) == 0: 
				new_problem.save()

	
	return

def codeforces_update_contest():
	url = "https://codeforces.com/api/contest.list"
	res = requests.get(url)
	data = res.json()

	if(data["status"] != 'OK') :
		return 

	organization_contest_participation.objects.all().update(current = 0)
	country_contest_participation.objects.all().update(current = 0)

	for codeforces_contest in data["result"]:

		url = "https://codeforces.com/api/contest.ratingChanges?contestId=" + str(codeforces_contest['id'])
		res = requests.get(url)
		data = res.json()

		if(data["status"] != 'OK') :
			continue

		new_contest,created = contest.objects.get_or_create(
			contestId = str(codeforces_contest['id']) , 
			defaults = {
				'Type' : 'R',
				'name' : codeforces_contest['name'],
				'duration' : codeforces_contest['durationSeconds'],
			}
		)
		if 'startTimeSeconds' in codeforces_contest:
			new_contest.startTime = codeforces_contest['startTimeSeconds']

		new_contest.participants = len(data['result'])
		new_contest.save()

		for participant in data['result']:
			user_handle = participant['handle']
			rank = participant['rank']

			try:
				contest_user = user.objects.get(handle = user_handle)
			except ObjectDoesNotExist:
				continue

			ucr,created = user_contest_rank.objects.get_or_create(user = contest_user , 
															contest = new_contest)

			ucr.worldRank = rank

			if contest_user.organization : 
				contest_user_org = contest_user.organization
				
				# check for organization_contest_participation 

				org_contest_participation,created = organization_contest_participation.objects.get_or_create(
					organization = contest_user_org,
					contest = new_contest,
					defaults= {
						'current' : '0',
						'total' : '0'
					}
				)
				org_contest_participation.current = str(int(org_contest_participation.current) + 1)
				if int(org_contest_participation.current) > int(org_contest_participation.total) :
					org_contest_participation.total = org_contest_participation.current

				org_contest_participation.save()
				ucr.organizationRank = org_contest_participation.current

			if contest_user.country : 

				contest_user_country = contest_user.country

				# check for country_contest_participation

				cntry_contest_participation,created = country_contest_participation.objects.get_or_create(
					country = contest_user_country,
					contest = new_contest,
					defaults= {
						'current' : '0',
						'total': '0'
					}
				)
				cntry_contest_participation.current = str(int(cntry_contest_participation.current) + 1)
				
				if int(cntry_contest_participation.current) > int(cntry_contest_participation.total) :
					cntry_contest_participation.total = cntry_contest_participation.current
				
				cntry_contest_participation.save()
				ucr.countryRank = cntry_contest_participation.current

			ucr.save()
	return

def update_codeforces():
	subject = 'Codeforces update Started'
	message = 'This is automated message from Codedigger which tells that your codeforces updation has started'
	recepient = 'shivamsinghal1012@gmail.com'
	send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

	alter_tables()
	codeforces_update_users()
	codeforces_update_problems()
	codeforces_update_contest()

	subject = 'Codeforces update Finished'
	message = 'This is automated message from Codedigger which tells that your codeforces updation has finished'
	recepient = 'shivamsinghal1012@gmail.com'
	send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
	

