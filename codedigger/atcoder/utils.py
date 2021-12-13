import re
import json
import requests
from bs4 import BeautifulSoup as bs4
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .api import *
from .scrapers_utils import get_all_contests_details
from .scrapers import get_user_history
from lists.utils import get_next_url, get_prev_url, get_total_page
from user.exception import ValidationException
from codeforces.api import user_status


def atcoder_status(handle):

    res = get_user_history(handle)

    contests_details = set()
    all_contest = set()
    solved = set()
    wrong = set()

    if res.status_code != 200:
        return (contests_details, all_contest, solved, wrong)

    contests_details = get_all_contests_details(res.content)

    res = get_user_results(handle)

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
