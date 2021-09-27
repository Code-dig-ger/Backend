import os
import requests
import random
import re
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def login():
    # To Login to Codeforces
    url = "https://codeforces.com/enter"
    res = requests.get(url)
    soup = bs(res.content, features="html5lib")
    Cookie = res.headers['Set-Cookie'][:47] + res.headers['Set-Cookie'][66:81]
    CsrfToken = soup.find('meta', {'name': 'X-Csrf-Token'})['content']
    ftaa = ''.join(
        random.choices(
            'abcdefghijklmnopqrstuvwxyz0123456789',
            k=18))

    headers = {
        'Cookie': Cookie,
        'Host': 'codeforces.com',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'X-Csrf-Token': CsrfToken
    }

    body = {
        'csrf_token': CsrfToken,
        'action': 'enter',
        'ftaa': ftaa,
        'bfaa': 'f1b3f18c715565b589b7823cda7448ce',
        'handleOrEmail': os.getenv('CODEFORCES_HANDLE'),
        'password': os.getenv('CODEFORCES_PASSWORD'),
        '_tta': '176',
        'remember': 'on'
    }

    res = requests.post(url, headers=headers, data=body)
    Cookie = res.headers['Set-Cookie'][:47] + \
        res.headers['Set-Cookie'][66:81] + res.headers['Set-Cookie'][146:199]
    return Cookie


def clean(s):
    # Remove Space Tab Newline
    return re.sub(r"[\n\t\s\r]*", "", s)


def penalty(cookie, contestId, subId, groupId):
    # Short Code Contest Penalty
    url = "https://codeforces.com/group/" + \
        str(groupId) + "/contest/" + str(contestId) + "/submission/" + str(subId)
    res = requests.get(url, headers={'Cookie': cookie})
    soup = bs(res.content, features="html5lib")
    return len(clean(soup.find('pre', {'id': 'program-source-text'}).text))
