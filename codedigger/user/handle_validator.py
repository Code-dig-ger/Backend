import requests
import bs4


def check_handle_cf(handle):
    req = requests.get(' https://codeforces.com/api/user.info?handles=' + handle)
    if req.status_code == 200:
        return True
    return False

def check_handle_spoj(user):
    url = 'https://www.spoj.com/users/'+user
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    profile = soup.find('div' , {'id' : 'user-profile-left'})
    return False if profile == None else True

def check_handle_codechef(user):
    url = 'https://codechef.com/users/' + user
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    profile = soup.find('section' , {'class' : 'user-details'})
    if profile is None:
        return False
    return True

def check_handle_atcoder(user):
    url = 'https://atcoder.jp/users/' + user
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    profile = soup.find('div' , {'class' : 'col-md-3 col-sm-12'})
    if profile is None:
        return False
    return True

def check_handle_uva(handle):
    req = requests.get(' https://uhunt.onlinejudge.org/api/uname2uid/' + handle)
    return req.text != '0'

def get_uva(handle):
    req = requests.get(' https://uhunt.onlinejudge.org/api/uname2uid/' + handle)
    return req.text