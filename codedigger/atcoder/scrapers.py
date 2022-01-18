import requests
from utils.exception import ValidationException

BASEURL = "https://atcoder.jp"


def get_user_history(handle):
    url = BASEURL + "/users/" + handle + "/history"
    res = requests.get(url)
    if res.status_code != 200:
        raise ValidationException('User not found in Atcoder')
    return res


def get_user_profile(handle):
    url = BASEURL + "/users/" + handle
    res = requests.get(url)
    if res.status_code != 200:
        raise ValidationException('User not found in Atcoder')
    return res
