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
