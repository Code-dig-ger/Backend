import requests
from bs4 import BeautifulSoup
from time import sleep
import os, json, django

from .models import CodechefContest, CodechefContestProblems
from problem.models import Problem


def ContestProblemScraper(code):
    link = f"https://www.codechef.com/{code}/problems/"
    query_problem_url = f"https://www.codechef.com/api/contests/" + code
    problem_req = requests.get(query_problem_url)
    if problem_req.status_code != 200:
        # raise Validation
        return
    problem_req = problem_req.json()
    plat = 'C'

    # return problem_req["problems"]

    for prob_code in problem_req["problems"]:
        prob_info = Problem(name=problem_req["problems"][prob_code]["name"],
                            prob_id=prob_code,
                            url=link + prob_code,
                            contest_id=code,
                            platform=plat)
        # print(problem_req["problems"][prob_code]["name"]+ " " + prob_code + " " + link+prob_code + " " + code)
        prob_info.save()
        contest_info = CodechefContest.objects.get(contestId=code)
        complete_prob_info = CodechefContestProblems(contest=contest_info,
                                                     problem=prob_info)
        complete_prob_info.save()


# def contestData():


def ContestScraper(num=0):

    query_url = f"https://www.codechef.com/api/list/contests/past?sort_by=START&sorting_order=desc&offset={num}&mode=premium"
    # Query URL might change in future.
    req = requests.get(query_url)

    if req.status_code != 200:
        return
    contests_code = []
    req = req.json()
    for cont in reversed(req['contests']):
        contest_name = cont['contest_name']
        code = cont['contest_code']
        timeDuration = cont['contest_duration']
        startDateTime = cont['contest_start_date']
        contest_access_url = "https://www.codechef.com/"
        cont_url = "https://www.codechef.com/api/contests/" + code
        cont_req = requests.get(cont_url)
        if cont_req.status_code != 200:
            break
        cont_req = cont_req.json()

        if cont_req['is_a_parent_contest'] != True:
            contest = CodechefContest(name=contest_name,
                                      contestId=code,
                                      duration=timeDuration,
                                      startTime=startDateTime,
                                      division='',
                                      url=contest_access_url + code)

            if CodechefContest.objects.filter(contestId=code).exists():
                continue

            contest.save()
            ContestProblemScraper(code)

        else:
            for div in cont_req['child_contests']:
                contest_code = cont_req['child_contests'][div]['contest_code']
                if div == "all":
                    continue
                contest = CodechefContest(name=contest_name,
                                          contestId=contest_code,
                                          duration=timeDuration,
                                          startTime=startDateTime,
                                          division=div,
                                          url=contest_access_url +
                                          contest_code)

                if CodechefContest.objects.filter(
                        contestId=contest_code).exists():
                    continue

                contest.save()
                ContestProblemScraper(contest_code)


def go_scraper():
    for i in range(40, -1, -20):
        ContestScraper(i)
