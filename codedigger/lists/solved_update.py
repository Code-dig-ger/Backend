import requests
import bs4

import os,django,json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codedigger.settings")
django.setup()
from lists.models import Solved
from user.models import Profile,User
from problem.models import Problem


def codechef(user,prob_id):
    if user is None or user == "":
        return
    if Solved.objects.filter(problem__prob_id=prob_id,user__username=user).exists():
        return
    codechef_handle = Profile.objects.get(owner__username=user).codechef
    if codechef_handle is None:
        return
    url = 'https://www.codechef.com/users/'+str(codechef_handle)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    problems_solved = soup.find('section' , {'class' : 'rating-data-section problems-solved'})
    if problems_solved.find('h5').text == 'Fully Solved (0)':
        return
    probset = set([])
    for ele in problems_solved.find('article').find_all('a'):
        probset.add(ele.text)
    if prob_id in probset:
        print("Adding " + prob_id)
        user = User.objects.get(username=user)
        #testing purposes
        if not Problem.objects.filter(prob_id=prob_id,platform='C').exists():
            return
        prob = Problem.objects.get(prob_id=prob_id)
        Solved.objects.create(user=user,problem=prob)
    
        


def spoj(user,prob_id):
    if user is None or user == "":
        return
    if Solved.objects.filter(problem__prob_id=prob_id,user__username=user).exists():
        return
    spoj_handle = Profile.objects.get(owner__username = user).spoj
    if spoj_handle == None:
        return
    url = 'https://www.spoj.com/status/'+ str(prob_id) + ',' + str(spoj_handle)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    status = soup.find('td' , {'status' : '15'})
    if status is not None:
        print(str(prob_id))
        prob = Problem.objects.get(prob_id=prob_id,platform='S')
        curr_user = User.objects.get(username=user)
        Solved.objects.create(user=curr_user,problem=prob)


def codeforces(user):
    if user is None or user == "":
        return
    cf_handle = Profile.objects.get(owner__username = user).codeforces
    if cf_handle == None:
        return
    url = 'https://codeforces.com/api/user.status?handle=' + user
    req = requests.get(url).json()
    limit = 10
    for ele in req['result']:
        name = ele['problem']['name']
        verdict = None
        verdict = ele['verdict']
        if verdict is None:
            continue
        prob_id = str(ele['problem']['contestId']) + str(ele['problem']['index'])
        print(name + " " + verdict + " " + prob_id)
        if verdict == "OK":
            solve = Solved.objects.filter(user__username=user,problem__prob_id = prob_id).exists()
            if solve:
                limit -= 1
                if limit <= 0:
                    break
                continue
            else:
                curr_user = User.objects.get(username=user)
                #next if block below only for testing as the problem needs to exist in the database to get it 
                if not Problem.objects.filter(prob_id=prob_id,platform='F').exists():
                    continue
                prob = Problem.objects.get(prob_id=prob_id,platform='F')
                Solved.objects.create(user=curr_user,problem=prob)
    
def uva(user):
    if user is None or user == "":
        return
    uva_id = Profile.objects.get(owner__username = user).uva_id
    if uva_id is None:
        return
    url1 = "https://uhunt.onlinejudge.org/api/subs-user/" + str(uva_id)
    req1 = requests.get(url1).json()
    sorted_req1 = sorted(req1['subs'],key=lambda k: k[4], reverse=True)
    limit = 10
    for ele in sorted_req1:
        print(str(ele[1]) + " " + str(ele[2])) 
        if str(ele[2]) != '90':
            continue
        #testing
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
    if user is None or user == "":
        return
    atcoder_handle = Profile.objects.get(owner__username = user).atcoder
    if atcoder_handle is None:
        return
    url = 'https://kenkoooo.com/atcoder/atcoder-api/results?user=' + atcoder_handle
    req = requests.get(url).json()
    sorted_req = sorted(req,key=lambda k: k['epoch_second'], reverse=True)
    limit = 10
    for ele in sorted_req:
        print(ele['problem_id'] + " " + ele['result'])
        if ele['result'] != "AC":
            continue
        #testing
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

# url = 'https://www.spoj.com/users/'+spoj_handle
    # res = requests.get(url)
    # soup = bs4.BeautifulSoup(res.content,'html.parser')
    # problems = soup.find('table' , {'class' : 'table table-condensed'})
    # if problems is None:
    #     return
    # for ele in problems.find_all('td'):
    #     if ele.text == "":
    #         continue
    #     curr_user = User.objects.filter(username=user)[0]
    #     prob = Problem.objects.filter(prob_id = ele.text)[0]
    #     if not prob:
    #         continue
    #     qs = Solved.objects.filter(user=curr_user,problem=prob)
    #     if not qs:
    #         Solved.objects.create(user=curr_user,problem=prob)