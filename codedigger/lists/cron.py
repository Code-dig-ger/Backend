import requests
import bs4

import os,django,json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codedigger.settings")
django.setup()
from lists.models import Solved
from user.models import Profile,User
from problem.models import Problem
from django.core.mail import send_mail	
from codedigger.settings import EMAIL_HOST_USER

def cron_codeforces(user):
    if user is None:
        return
    cf_handle = Profile.objects.get(owner = user).codeforces
    if cf_handle == None:
        return
    url = 'https://codeforces.com/api/user.status?handle=' + cf_handle
    req = requests.get(url)
    if req.status_code != 200:
        return 
    req = req.json()
    if req['status'] != 'OK':
        return
    limit = 10
    for ele in req['result']:
        if 'verdict' not in ele or 'contestId' not in ele or ele['verdict'] != 'OK':
            continue
        prob_id = str(ele['problem']['contestId']) + str(ele['problem']['index'])
        prob = Problem.objects.filter(prob_id= prob_id , platform='F')
        if not prob.exists() :
            continue
        solve,created = Solved.objects.get_or_create(user=user,problem = prob[0])
        if not created:
            limit -= 1
            if limit <= 0:
                break
            continue
    
def cron_uva(user):
    if user is None:
        return
    uva_id = Profile.objects.get(owner = user).uva_id
    if uva_id is None:
        return
    url1 = "https://uhunt.onlinejudge.org/api/subs-user/" + str(uva_id)
    req1 = requests.get(url1)
    if req1.status_code != 200 :
        return 
    req1 = req1.json()
    sorted_req1 = sorted(req1['subs'],key=lambda k: k[4], reverse=True)
    limit = 10
    for ele in sorted_req1:
        if str(ele[2]) != '90':
            continue
        prob = Problem.objects.filter(prob_id=str(ele[1]),platform='U')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(user = user,problem = prob[0])
        if not created:
            limit -= 1
            if limit <= 0:
                break
            continue
    
def cron_atcoder(user):
    if user is None:
        return
    atcoder_handle = Profile.objects.get(owner = user).atcoder
    if atcoder_handle is None:
        return
    url = 'https://kenkoooo.com/atcoder/atcoder-api/results?user=' + atcoder_handle
    req = requests.get(url)
    if req.status_code != 200:
        return
    req = req.json()
    sorted_req = sorted(req,key=lambda k: k['epoch_second'], reverse=True)
    limit = 10
    for ele in sorted_req:
        if ele['result'] != "AC":
            continue
        prob = Problem.objects.filter(prob_id=ele['problem_id'],platform='A')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(user = user,problem = prob[0])
        if not created:
            limit -= 1
            if limit <= 0:
                break
            continue

def cron_codechef(user):
    if user is None:
        return
    codechef_handle = Profile.objects.get(owner=user).codechef
    if codechef_handle is None:
        return
    url = 'https://www.codechef.com/users/'+str(codechef_handle)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    problems_solved = soup.find('section' , {'class' : 'rating-data-section problems-solved'})
    if problems_solved is None:
        return
    if problems_solved.find('h5').text == 'Fully Solved (0)':
        return
    for ele in problems_solved.find('article').find_all('a'):
        prob = Problem.objects.filter(prob_id=ele.text,platform='C')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(problem=prob[0],user=user)

def cron_spoj(user):
    if user is None:
        return
    spoj_handle = Profile.objects.get(owner= user).spoj
    if spoj_handle == None:
        return
    url = 'https://www.spoj.com/users/'+spoj_handle
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    problems = soup.find('table' , {'class' : 'table table-condensed'})
    if problems is None:
        return
    for ele in problems.find_all('td'):
        if ele.text == "":
            continue
        prob = Problem.objects.filter(prob_id = ele.text,platform='S')
        if not prob.exists():
            continue
        solve, created = Solved.objects.get_or_create(problem=prob[0],user=user)

def updater():
    subject = 'Codeforces update Problems Started'
    message = 'This is automated message from Codedigger which tells that your codeforces updation has started'
    recepient = 'aaradhyaberi@gmail.com'
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    for ele in User.objects.all():
        cron_codeforces(ele)
        cron_uva(ele)
        cron_atcoder(ele)
        cron_codechef(ele)
        cron_spoj(ele)
    subject = 'Codeforces update Problems Started'
    message = 'This is automated message from Codedigger which tells that your codeforces updation has ended'
    recepient = 'aaradhyaberi@gmail.com'
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

msg = '{} Update List {}'

def codeforces_updater():
    send_mail(msg.format('Codeforces','Started'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)
    for ele in User.objects.all():
        cron_codeforces(ele)
    send_mail(msg.format('Codeforces','Finished'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)

def uva_updater():
    send_mail(msg.format('Uva','Started'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)
    for ele in User.objects.all():
        cron_uva(ele)
    send_mail(msg.format('Uva','Finished'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)

def codechef_updater():
    send_mail(msg.format('Codechef','Started'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)
    for ele in User.objects.all():
        cron_codechef(ele)
    send_mail(msg.format('Codechef','Finished'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)

def atcoder_updater():
    send_mail(msg.format('Atcoder','Started'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)
    for ele in User.objects.all():
        cron_atcoder(ele)
    send_mail(msg.format('Atcoder','Finished'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)

def spoj_updater():
    send_mail(msg.format('Spoj','Started'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)
    for ele in User.objects.all():
        cron_spoj(ele)
    send_mail(msg.format('Spoj','Finished'), 'OK', EMAIL_HOST_USER, ['testing.codedigger@gmail.com'], fail_silently = True)


def codechef_list(user):
    if user is None or user == "":
        return
    codechef_handle = Profile.objects.get(owner__username=user).codechef
    if codechef_handle is None:
        return
    url = 'https://www.codechef.com/users/'+str(codechef_handle)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    problems_solved = soup.find('section' , {'class' : 'rating-data-section problems-solved'})
    if problems_solved.find('h5').text == 'Fully Solved (0)':
        return []
    prob_list = set()
    for ele in problems_solved.find('article').find_all('a'):
        #testing purposes
        if not Problem.objects.filter(prob_id=ele.text,platform='C').exists():
            continue
        prob_list.add(prob_id)
    return prob_list
        