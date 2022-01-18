import re
import json
import requests
from bs4 import BeautifulSoup as bs4
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from lists.utils import (sub_page_number, get_next_url, get_prev_url,
                         get_total_page, getqs)
from utils.exception import ValidationException
from codeforces.api import user_status

from .serializers import ProbSerializer


def codeforces_status(handle):
    # Deprecated

    RContest = set()
    VContest = set()
    SolvedInContest = set()
    Upsolved = set()
    Wrong = set()
    try:
        submissions = user_status(handle=handle)
    except ValidationError:
        return (RContest, VContest, SolvedInContest, Upsolved, Wrong)
    for submission in submissions:
        if 'contestId' in submission:
            # to be sure this is a contest problem
            contestId = submission['contestId']

            if submission['author']['participantType'] == 'CONTESTANT':
                RContest.add(contestId)
            elif submission['author']['participantType'] != 'PRACTICE':
                VContest.add(contestId)

            if 'verdict' in submission:
                # to be sure verdict is present
                if submission['verdict'] == 'OK':
                    if submission['author']['participantType'] != 'PRACTICE':
                        SolvedInContest.add(
                            str(submission['problem']['contestId']) +
                            submission['problem']['index'])
                    else:
                        Upsolved.add(
                            str(submission['problem']['contestId']) +
                            submission['problem']['index'])
    for submission in submissions:
        if 'contestId' in submission:
            if 'verdict' in submission:
                # to be sure verdict is present
                prob_id = str(submission['problem']
                              ['contestId']) + submission['problem']['index']
                if submission[
                        'verdict'] != 'OK' and prob_id not in SolvedInContest and prob_id not in Upsolved:
                    Wrong.add(prob_id)

    return (RContest, VContest, SolvedInContest, Upsolved, Wrong)


def codechef_status(handle):

    Practice = set()
    SolvedInContest = set()
    Contest = set()
    ContestName = {}

    url = "https://www.codechef.com/users/" + handle

    res = requests.get(url)
    if res.status_code != 200:
        return (Practice, SolvedInContest, Contest, ContestName)

    soup = bs4(res.content, 'html5lib')
    finding_rating = re.findall(r'var all_rating = .*;', str(soup))
    finds = len(finding_rating) == 1

    if finds:
        s = finding_rating[0].replace('var all_rating = ', '').replace(';', '')
        contest_details = json.loads(s)
        del s
        del finding_rating

    Contest = set()
    ContestName = {}
    for contest in contest_details:
        Contest.add(contest['code'])
        ContestName[contest['code']] = contest['name']

    problems_solved = soup.find(
        'section', {'class': 'rating-data-section problems-solved'})

    del soup

    if problems_solved.find('h5').text == 'Fully Solved (0)':
        return (Practice, SolvedInContest, Contest, ContestName)
    else:

        FullySolved = problems_solved.find('article')
        del problems_solved

        if FullySolved.find('p').find('strong').text == 'Practice:':
            Practice = {x.text for x in FullySolved.find('p').findAll('a')}
            SolvedInContest = set()
            for y in FullySolved.findAll('p')[1:]:
                for x in y.findAll('a'):
                    SolvedInContest.add(x.text)
        else:
            SolvedInContest = {
                x.text
                for x in problems_solved.find('article').findAll('a')
            }

    return (Practice, SolvedInContest, Contest, ContestName)


def atcoder_status(handle):

    url = "https://atcoder.jp/users/" + handle + "/history"
    res = requests.get(url)

    contests_details = set()
    all_contest = set()
    solved = set()
    wrong = set()

    if res.status_code != 200:
        return (contests_details, all_contest, solved, wrong)

    soup = bs4(res.content, 'html5lib')
    contestTable = soup.find('table', {'id': 'history'})
    del soup
    if contestTable != None:
        contests = contestTable.find('tbody').findAll('tr')
        del contestTable
        for contest in contests:
            contests_details.add(
                contest.findAll('td')[1].find('a')['href'].split('/')[-1])
        del contests

    url = "https://kenkoooo.com/atcoder/atcoder-api/results?user=" + handle
    res = requests.get(url)
    if res.status_code != 200:
        return (contests_details, all_contest, solved, wrong)

    data = res.json()

    for sub in data:
        all_contest.add(sub["contest_id"])
        if sub["result"] == "AC":
            solved.add(sub["problem_id"])

    for sub in data:
        if sub["result"] != "AC" and sub["problem_id"] not in solved:
            wrong.add(sub["problem_id"])

    return (contests_details, all_contest, solved, wrong)


def get_page_number(page, default=1):
    if page == None:
        return default
    elif page.isdigit():
        return int(page)
    else:
        raise ValidationException('Page must be an integer.')


def get_problem_filter_response(user, page_number, per_page, url, problem_qs):
    # param:
    # user:			Object of User Model
    # page_number: 	Current Page Number
    # per_page: 	number of problems in a page
    # url:			Base url
    # problem_qs:	List of Problems Total

    if not user.is_authenticated:
        user = None
    total_problems = problem_qs.count()
    total_page = get_total_page(total_problems, per_page)

    if page_number > total_page:
        raise ValidationException('Page Number Out of Bound')

    qs = getqs(problem_qs, per_page, page_number)

    res = {
        "status": "OK",
        "result": ProbSerializer(qs, many=True, context={
            "user": user
        }).data,
        'link': {
            'first': sub_page_number(url, 1),
            'last': sub_page_number(url, total_page),
            'prev': get_prev_url(page_number, url),
            'next': get_next_url(page_number, url, total_page),
        },
        'meta': {
            'current_page': page_number,
            'from': (page_number - 1) * per_page + 1,
            'last_page': total_page,
            'path': url,
            'per_page': per_page,
            'to':
            total_problems if page_number == total_page else page_number *
            per_page,
            'total': total_problems
        }
    }
    return res


def get_upsolve_response_dict(user_contest_details, path, page, total_contest,
                              per_page):

    total_page = get_total_page(total_contest, per_page)
    Prev = get_prev_url(page, path)
    Next = get_next_url(page, path, total_page)

    return {
        'status': 'OK',
        'result': user_contest_details,
        'links': {
            'first': path + 'page=1',
            'last': path + 'page=' + str(total_page),
            'prev': Prev,
            'next': Next
        },
        'meta': {
            'current_page': page,
            'from': (page - 1) * per_page + 1,
            'last_page': total_page,
            'path': path,
            'per_page': per_page,
            'to': total_contest if page == total_page else page * per_page,
            'total': total_contest
        }
    }
