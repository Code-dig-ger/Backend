import requests
import bs4


def check_handle_cf(handle):
    if handle is None:
        return 0
    req = requests.get(
        ' https://codeforces.com/api/user.info?handles=' +
        handle)
    if req.status_code >= 500:
        return 1
    if req.status_code == 200:
        return 2
    return 0


def check_handle_spoj(user):
    if user is None:
        return True
    url = 'https://www.spoj.com/users/' + user
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    profile = soup.find('div', {'id': 'user-profile-left'})
    return False if profile is None else True


def check_handle_codechef(user):
    if user is None:
        return True
    url = 'https://codechef.com/users/' + user
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    profile = soup.find('section', {'class': 'user-details'})
    if profile is None:
        return False
    return True


def check_handle_atcoder(user):
    if user is None:
        return True
    url = 'https://atcoder.jp/users/' + user
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    profile = soup.find('div', {'class': 'col-md-3 col-sm-12'})
    if profile is None:
        return False
    return True


def check_handle_uva(handle):
    if handle is None:
        return True
    req = requests.get(
        ' https://uhunt.onlinejudge.org/api/uname2uid/' +
        handle)
    return req.text != '0'


def get_uva(handle):
    if handle is None:
        return None
    req = requests.get(
        ' https://uhunt.onlinejudge.org/api/uname2uid/' +
        handle)
    return req.text
