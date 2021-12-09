import requests
from bs4 import BeautifulSoup
from time import sleep
import os, json, django
from user.exception import ValidationException


def divisionScraper(contest_id):

    contest_url = f"https://www.codechef.com/api/contests/{contest_id}"
    contest_req = requests.get(contest_url)
    if contest_req.status_code != 200:
        raise ValidationException(
            'Failed Scrapping Codechef Contest Divisions')

    contest_req = contest_req.json()
    return contest_req


def contestScraper(offset, contest_type):

    query_contest_url = f"https://www.codechef.com/api/list/contests/{contest_type}?sort_by=START&sorting_order=desc&offset={offset}&mode=premium"
    # Query URL might change in future.
    contest_data = requests.get(query_contest_url)

    if contest_data.status_code != 200:
        raise ValidationException('Failed Scrapping Codechef Contests')

    contest_data = contest_data.json()

    return contest_data


def problemScraper(contest_code):

    query_problem_url = f"https://www.codechef.com/api/contests/{contest_code}"
    # Query URL might change in future.
    problem_data = requests.get(query_problem_url)
    if problem_data.status_code != 200:
        raise ValidationException('Failed Scrapping Codechef Problems')

    problem_data = problem_data.json()

    return problem_data

def UserSubmissionDetail(problemcode, user):
    URL = "https://www.codechef.com/SNCKQL21/status/{problemcode},{user}"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    problemTable = soup.findAll('table', class_ = "dataTable")
    problemRow = problemTable[0].findAll('tr')
    submissionList = []
    for problem in problemRow:
        problemDetails = i.findAll('td')
        for details in problemDetails:
            print(details)

    return submissionList
    

def recentSubmissions(user):
    URL = "https://www.codechef.com/recent/user?user_handle={user}"
    r = requests.get(URL)
    r = BeautifulSoup(r.content, 'html5lib')
    recentSubs = r.findAll('tr')
    recentList = []
    for sub in recentSubs:
        subd = sub.findAll('td')
        print(subd)

    return returnList