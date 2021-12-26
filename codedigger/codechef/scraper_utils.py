import requests
from bs4 import BeautifulSoup
from time import sleep
import os, json, django
from user.exception import ValidationException
from codechef.scraper import contestScraper, problemScraper, divisionScraper


def OffsetLoader(contest_type):

    requested_contests = []
    for i in range(0, 60,
                   20):  #offset {0, 20, 40} for multiple pages of contests.
        contests_data = contestScraper(i, contest_type)

        for contests in contests_data['contests']:
            requested_contests.append(contests)

    return requested_contests


def getContestDivision(contest_id):

    contest_req = problemScraper(contest_id)
    subcontests = []
    if contest_req['is_a_parent_contest'] != True:
        subcontests.append(contest_id)
    else:
        for div in contest_req['child_contests']:
            if div == "all":
                continue
            contest_code = contest_req['child_contests'][div]['contest_code']
            subcontests.append(contest_code)

    return subcontests


def ContestData(type):

    contests_data = OffsetLoader(type)
    all_contests = []
    dateDict = {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December"
    }
    for contest in contests_data:
        childContests = getContestDivision(contest['contest_code'])

        for contest_id in childContests:
            contest_temp_date = contest['contest_start_date']
            contest_updated_date = contest_temp_date[:3] + dateDict[
                contest_temp_date[3:6]] + contest_temp_date[6:]
            finalContestData = {
                "Name": contest['contest_name'],
                "ContestCode": contest_id,
                "Duration": contest['contest_duration'],
                "StartTime": contest_updated_date,
                'ContestURL': "https://www.codechef.com/" + contest_id
            }

            all_contests.append(finalContestData)

    return all_contests


def ProblemData(contest_code):
    problem_url_temp = f"https://www.codechef.com/{contest_code}/problems/"
    platform = 'C'

    problem_data = problemScraper(contest_code)
    all_problems = []

    for prob_code in problem_data["problems"]:
        finalProblemData = {
            "Name": problem_data["problems"][prob_code]["name"],
            "ProblemCode": prob_code,
            "ProblemURL": problem_url_temp + prob_code,
            "ContestId": contest_code,
            "Platform": platform
        }
        all_problems.append(finalProblemData)

    return (all_problems)
