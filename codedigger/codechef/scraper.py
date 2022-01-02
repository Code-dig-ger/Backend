import requests
from bs4 import BeautifulSoup

from user.exception import ValidationException

from problem.models import *
from codechef.models import *


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
    # Query URL might change inuserid future.
    problem_data = requests.get(query_problem_url)
    if problem_data.status_code != 200:
        raise ValidationException('Failed Scrapping Codechef Problems')

    problem_data = problem_data.json()

    return problem_data


def UserSubmissionScraper(problemcode, contest, user):

    URL = f"https://www.codechef.com/{contest}/status/{problemcode},{user}"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup


def recentSubmissionScraper(user_handle):
    
    URL = f"https://www.codechef.com/recent/user?user_handle={user_handle}"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup


def profilePageScraper(user_handle):

    query_user_profile_url = f"https://www.codechef.com/users/{user_handle}"
    r = requests.get(query_user_profile_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
