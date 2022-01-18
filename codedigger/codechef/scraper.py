import requests
from bs4 import BeautifulSoup

from utils.exception import ValidationException

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


def UserSubmissionDetail(problemcode, contest, user):
    URL = f"https://www.codechef.com/{contest}/status/{problemcode},{user}"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    problemTable = soup.findAll('table', class_="dataTable")
    problemRow = problemTable[0].findAll('tr')
    problemRow.pop(0)
    submissionlist = []
    if len(problemRow) == 0 or problemRow[0].text == 'No Recent Activity':
        return submissionlist

    for problem in problemRow:
        baseurl = "https://www.codechef.com"
        problemDetails = problem.findAll('td')
        subid = problemDetails[0].text
        subtime = problemDetails[1].text
        verdict = problemDetails[3].find('span').get('title')
        if len(verdict) == 0:
            verdict = (problemDetails[3].find('span').text)
            verdict = verdict[:verdict.index('[')]
            if int(verdict) == 100:
                verdict = "accepted [100/100]"
            else:
                verdict = "partially accepted [" + verdict + "/100]"
        lang = problemDetails[6].text
        link = baseurl + problemDetails[7].find('a').get('href')

        subformat = {
            'subid': subid,
            'subtime': subtime,
            'verdict': verdict,
            'lang': lang,
            'link': link,
        }

        submissionlist.append(subformat)

    return submissionlist


def recentSubmissions(userid):
    URL = f"https://www.codechef.com/recent/user?user_handle={userid}"
    r = requests.get(URL)
    r = BeautifulSoup(r.content, 'html5lib')
    recentSubs = r.findAll('tbody')

    recentlist = []
    for sub in recentSubs:
        subd = sub.findAll('tr')
        subd.pop(-1)
        try:
            query = subd[0].text[:18]
        except:
            query = "Profile found successfully"
        if query == 'No Recent Activity':
            break

        for prob in subd:
            baseurl = "https://www.codechef.com"
            det = prob.findAll('td')

            probid = det[1].find('a').text
            probid = probid[:probid.index('<')]

            link = det[1].find('a').get('href')
            link = link.replace("\\", "")
            link = baseurl + link

            subtime = prob.find('span', class_="tooltiptext")
            try:
                subtime = subtime.text
                subtime = subtime[:subtime.index('<')]
            except:
                break

            verdict = det[2].find('span').get('title')
            if len(verdict) == 0:
                verdict = (det[2].find('span').text)
                verdict = verdict[:verdict.index('[')]
                if int(verdict) == 100:
                    verdict = "accepted [100/100]"
                else:
                    verdict = "partially accepted [" + verdict + "/100]"

            lang = det[3].text
            lang = lang[:lang.index('<')]

            subformat = {
                'probid': probid,
                'subtime': subtime,
                'verdict': verdict,
                'lang': lang,
                'link': link,
            }

            recentlist.append(subformat)

    return recentlist


def profilePageScraper(user_handle):

    query_user_profile_url = f"https://www.codechef.com/users/{user_handle}"
    r = requests.get(query_user_profile_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
