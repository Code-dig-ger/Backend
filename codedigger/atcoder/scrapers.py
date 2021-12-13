import requests
from math import log2
from problem.models import Problem, atcoder_contest
from .api import * 
from utils.common import rating_to_difficulty

def get_user_history(handle):
    url = "https://atcoder.jp/users/" + handle + "/history"
    res = requests.get(url)
    return res
