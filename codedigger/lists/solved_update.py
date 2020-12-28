import requests
import bs4

import os,django,json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codedigger.settings")
django.setup()
from lists.models import Solved
from user.models import Profile,User
from problem.models import Problem


# def codechef(user):
#     if user is None:
#         return
#     url = 'https://www.codechef.com/users/'+user
#     res = requests.get(url)
#     soup = bs4.BeautifulSoup(res.content,'html.parser')
#     problems_solved = soup.find('section' , {'class' : 'rating-data-section problems-solved'})
#     if problems_solved.find('h5').text == 'Fully Solved (0)':
#         return
#     for ele in problems_solved.find('article').find_all('a'):
#         curr_user = User.objects.filter(username = user).first()
#         prob = Problem.objects.filter(prob_id = ele.text).first()
#         if not prob:
#             continue
#         qs = Solved.objects.filter(user=curr_user,problem=prob).first()
#         if not qs:
#             Solved.objects.create(user=curr_user,problem=prob)


# def spoj(user):
#     if user is None or user == "":
#         return
#     spoj_handle = Profile.objects.get(owner__username = user).spoj
#     if spoj_handle == None or spoj_handle == " ":
#         return
#     url = 'https://www.spoj.com/users/'+spoj_handle
#     res = requests.get(url)
#     soup = bs4.BeautifulSoup(res.content,'html.parser')
#     problems = soup.find('table' , {'class' : 'table table-condensed'})
#     if problems is None:
#         return
#     for ele in problems.find_all('td'):
#         if ele.text == "":
#             continue
#         curr_user = User.objects.filter(username=user)[0]
#         prob = Problem.objects.filter(prob_id = ele.text)[0]
#         if not prob:
#             continue
#         qs = Solved.objects.filter(user=curr_user,problem=prob)
#         if not qs:
#             Solved.objects.create(user=curr_user,problem=prob)

def codeforces(user):
    if user is None or user == "":
        return
    cf_handle = Profile.objects.get(owner__username = user).codeforces
    if cf_handle == None or cf_handle == " ":
        return
    url = 'https://codeforces.com/api/user.status?handle=' + user
    req = requests.get(url).json()
    limit = 15
    for ele in req['result']:
        name = ele['problem']['name']
        verdict = ele['verdict']
        contest_id = ele['problem']['contestId']
        print(name + " " + verdict + " " + str(contest_id))
        if verdict == "OK":
            solve = Solved.objects.filter(user__username=user,problem__name = name).exists()
            if solve:
                limit -= 1
                if limit <= 0:
                    break
                continue
            else:
                curr_user = User.objects.get(username=user)
                #next if block below only for testing as the problem needs to exist in the database to get it 
                if not Problem.objects.filter(name=name,contest_id=contest_id,platform='F').exists():
                    continue
                prob = Problem.objects.get(name=name,contest_id=contest_id,platform='F')
                Solved.objects.create(user=curr_user,problem=prob)
    
def uva(user):
    if user is None or user == " ":
        return
    uva_id = Profile.objects.get(owner__username = user).uva_id
    if uva_id is None or uva_id == " ":
        return
    url1 = "https://uhunt.onlinejudge.org/api/subs-user/" + str(uva_id)
    req1 = requests.get(url1).json()
    sorted_req1 = sorted(req1['subs'],key=lambda k: k[4], reverse=True)
    limit = 15
    for ele in sorted_req1:
        print(str(ele[1]) + " " + str(ele[2])) 
        if str(ele[2]) != '90':
            continue
        if not Problem.objects.filter(prob_id=ele[1],platform='U').exists():
                continue
        solve = Solved.objects.filter(user__username = user,problem__prob_id = ele[1]).exists()
        if solve:
            limit -= 1
            if limit <= 0:
                break
            continue
        prob = Problem.objects.get(prob_id=ele[1],platform='U')
        curr_user = User.objects.get(username=user)
        Solved.objects.create(user=curr_user,problem=prob)


    
def atcoder(user):
    if user is None or user == " ":
        return
    atcoder_handle = Profile.objects.get(owner__username = user).atcoder
    if atcoder_handle is None or atcoder_handle == " ":
        return
    url = 'https://kenkoooo.com/atcoder/atcoder-api/results?user=' + atcoder_handle
    req = requests.get(url).json()
    sorted_req = sorted(req,key=lambda k: k['epoch_second'], reverse=True)
    limit = 15
    for ele in sorted_req:
        print(ele['problem_id'] + " " + ele['result'])
        if ele['result'] != "AC":
            continue
        if not Problem.objects.filter(prob_id=ele['problem_id'],platform='A').exists():
            continue
        solve = Solved.objects.filter(user__username = user,problem__prob_id = ele['problem_id']).exists()
        if solve:
            limit -= 1
            if limit <= 0:
                break
            continue
        prob = Problem.objects.get(prob_id=ele['problem_id'],platform='A')
        curr_user = User.objects.get(username=user)
        Solved.objects.create(user=curr_user,problem=prob)
