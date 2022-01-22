import requests
import bs4

import os, django, json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codedigger.settings")
django.setup()
from lists.models import Solved
from user.models import Profile, User
from problem.models import Problem
from codeforces.api import user_status
from user.exception import ValidationException


def codechef(user, prob):
    if user is None or Solved.objects.filter(problem=prob, user=user).exists():
        return
    codechef_handle = Profile.objects.get(owner=user).codechef
    if codechef_handle is None:
        return
    url = 'https://www.codechef.com/users/' + str(codechef_handle)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    problems_solved = soup.find(
        'section', {'class': 'rating-data-section problems-solved'})
    if not problems_solved or problems_solved.find(
            'h5').text == 'Fully Solved (0)':
        return
    probset = set([])
    for ele in problems_solved.find('article').find_all('a'):
        probset.add(ele.text)
    if prob.prob_id in probset:
        Solved.objects.create(user=user, problem=prob)


def spoj(user, prob):
    if user is None or Solved.objects.filter(problem=prob, user=user).exists():
        return
    spoj_handle = Profile.objects.get(owner=user).spoj
    if spoj_handle == None:
        return
    url = 'https://www.spoj.com/status/' + str(
        prob.prob_id) + ',' + str(spoj_handle)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    status = soup.find('td', {'status': '15'})
    if status is not None:
        Solved.objects.create(user=user, problem=prob)


def codeforces(user):
    if user is None:
        return
    cf_handle = Profile.objects.get(owner=user).codeforces
    if cf_handle == None:
        return
    try:
        submission_user = user_status(cf_handle)
    except ValidationException:
        return
    limit = 10
    for ele in submission_user:
        if 'verdict' not in ele or 'contestId' not in ele or ele[
                'verdict'] != 'OK':
            continue
        prob_id = str(ele['problem']['contestId']) + str(
            ele['problem']['index'])
        prob = Problem.objects.filter(prob_id=prob_id, platform='F')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(user=user,
                                                      problem=prob[0])
        if not created:
            limit -= 1
            if limit <= 0:
                break
            continue
    # url = 'https://codeforces.com/api/user.status?handle=' + str(cf_handle)
    # res = requests.get(url)
    # if res.status_code != 200:
    # return
    # req = res.json()
    # if req['status'] != 'OK':
    # return


def uva(user):
    if user is None:
        return
    uva_id = Profile.objects.get(owner=user).uva_id
    if uva_id is None:
        return
    url1 = "https://uhunt.onlinejudge.org/api/subs-user/" + str(uva_id)
    req1 = requests.get(url1).json()
    sorted_req1 = sorted(req1['subs'], key=lambda k: k[4], reverse=True)
    limit = 10
    for ele in sorted_req1:
        if str(ele[2]) != '90':
            continue
        prob = Problem.objects.filter(prob_id=str(ele[1]), platform='U')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(user=user,
                                                      problem=prob[0])
        if not created:
            limit -= 1
            if limit <= 0:
                break
            continue


def atcoder(user):
    if user is None:
        return
    atcoder_handle = Profile.objects.get(owner=user).atcoder
    if atcoder_handle is None:
        return
    url = 'https://kenkoooo.com/atcoder/atcoder-api/results?user=' + str(
        atcoder_handle)
    req = requests.get(url).json()
    sorted_req = sorted(req, key=lambda k: k['epoch_second'], reverse=True)
    limit = 10
    for ele in sorted_req:
        if ele['result'] != "AC":
            continue
        prob = Problem.objects.filter(prob_id=ele['problem_id'], platform='A')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(user=user,
                                                      problem=prob[0])
        if not created:
            limit -= 1
            if limit <= 0:
                break
            continue


def atcoder_scraper_check(user, prob):
    if user is None or Solved.objects.filter(problem=prob, user=user).exists():
        return
    atcoder_handle = Profile.objects.get(owner=user).atcoder
    if atcoder_handle is None:
        return
    contest = prob.contest_id
    taskname = prob.prob_id
    URL = "https://atcoder.jp/contests/" + contest + "/submissions/?f.User=" + user.username + "&" + "f.Task=" + taskname
    r = requests.get(URL)
    soup = bs4.BeautifulSoup(r.content, 'html5lib')
    check = soup.find_all("span", {"class": "label label-success"})
    if check:
        Solved.objects.create(user=user, problem=prob)


def UpdateforUserCodeforces(user, limit):
    # limit should either be None, or be an integer greater than or equal to 1.
    if user is None:
        return (False, "Given User object cannot be None")
    cf_handle = Profile.objects.get(owner=user).codeforces
    if cf_handle == None:
        return (False, "cf_handle cannot be None.")
    try:
        submission_user = user_status(cf_handle)
    except ValidationException:
        return (False, "Not able to fetch submission data from codeforces.")
    for ele in submission_user:
        if 'verdict' not in ele or 'contestId' not in ele or ele[
                'verdict'] != 'OK':
            continue
        prob_id = str(ele['problem']['contestId']) + str(
            ele['problem']['index'])
        prob = Problem.objects.filter(prob_id=prob_id, platform='F')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(user=user,
                                                      problem=prob[0])
        if not created and limit != None:
            limit -= 1
            if limit <= 0:
                break
            continue
    return (True,
            "Submission data for the given user has been saved successfully.")


def UpdateforUserCodechef(user, limit):
    if user is None:
        return (False, "Given User object cannot be None")
    codechef_handle = Profile.objects.get(owner=user).codechef
    if codechef_handle is None:
        return (False, "codechef_handle cannot be None.")
    url = 'https://www.codechef.com/users/' + str(codechef_handle)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    problems_solved = soup.find(
        'section', {'class': 'rating-data-section problems-solved'})
    if problems_solved is None:
        return (
            True,
            "Submission data for the given user has been saved successfully.")
    if problems_solved.find('h5').text == 'Fully Solved (0)':
        return (
            True,
            "Submission data for the given user has been saved successfully.")
    for ele in problems_solved.find('article').find_all('a'):
        prob = Problem.objects.filter(prob_id=ele.text, platform='C')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(problem=prob[0],
                                                      user=user)
        if not created and limit != None:
            limit -= 1
            if limit <= 0:
                break
            continue
    return (True,
            "Submission data for the given user has been saved successfully.")


def UpdateforUserAtcoder(user, limit):
    if user is None:
        return (False, "Given User object cannot be None")
    atcoder_handle = Profile.objects.get(owner=user).atcoder
    if atcoder_handle is None:
        return (False, "atcoder_handle cannot be None.")
    url = 'https://kenkoooo.com/atcoder/atcoder-api/results?user=' + atcoder_handle
    req = requests.get(url)
    if req.status_code != 200:
        return (False, "User with the given handle does not exist.")
    req = req.json()
    sorted_req = sorted(req, key=lambda k: k['epoch_second'], reverse=True)
    for ele in sorted_req:
        if ele['result'] != "AC":
            continue
        prob = Problem.objects.filter(prob_id=ele['problem_id'], platform='A')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(user=user,
                                                      problem=prob[0])
        if not created and limit != None:
            limit -= 1
            if limit <= 0:
                break
            continue
    return (True,
            "Submission data for the given user has been saved successfully.")


def UpdateforUserSpoj(user, limit):
    if user is None:
        return (False, "Given User object cannot be None")
    spoj_handle = Profile.objects.get(owner=user).spoj
    if spoj_handle == None:
        return (False, "spoj_handle cannot be None.")
    url = 'https://www.spoj.com/users/' + spoj_handle
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    problems = soup.find('table', {'class': 'table table-condensed'})
    if problems is None:
        return (
            True,
            "Submission data for the given user has been saved successfully.")
    for ele in problems.find_all('td'):
        if ele.text == "":
            continue
        prob = Problem.objects.filter(prob_id=ele.text, platform='S')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(problem=prob[0],
                                                      user=user)
        if not created and limit != None:
            limit -= 1
            if limit <= 0:
                break
            continue
    return (True,
            "Submission data for the given user has been saved successfully.")


def UpdateforUserUva(user, limit):
    if user is None:
        return (False, "Given User object cannot be None")
    uva_id = Profile.objects.get(owner=user).uva_id
    if uva_id is None:
        return (False, "uva_id cannot be None.")
    url1 = "https://uhunt.onlinejudge.org/api/subs-user/" + str(uva_id)
    req1 = requests.get(url1)
    if req1.status_code != 200:
        return (False, "User with the given UVA-ID does not exist")
    req1 = req1.json()
    sorted_req1 = sorted(req1['subs'], key=lambda k: k[4], reverse=True)
    for ele in sorted_req1:
        if str(ele[2]) != '90':
            continue
        prob = Problem.objects.filter(prob_id=str(ele[1]), platform='U')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(user=user,
                                                      problem=prob[0])
        if not created and limit != None:
            limit -= 1
            if limit <= 0:
                break
            continue
    return (True,
            "Submission data for the given user has been saved successfully.")
