import requests
from user.exception import ValidationException


def get_user_history(handle):
    url = "https://atcoder.jp/users/" + handle + "/history"
    res = requests.get(url)
    if res.status_code != 200:
        raise ValidationException('User not found in Atcoder')
    return res
