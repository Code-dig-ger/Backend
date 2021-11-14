import requests
from user.exception import ValidationException

BASEURL = "https://kenkoooo.com/atcoder/"

def validated_response(response):
    if response.status_code != 200:
        raise ValidationException('Kenkoooo API: Bad Request')
    return response.json()

def get_all_contests():
    url = "resources/contests.json"
    res = requests.get(url)
    return validated_response(res)


def get_all_problems():
    url = "resources/problems.json"
    res = requests.get(url)
    return validated_response(res)


def get_all_problems_models():
    url = "resources/problem-models.json"
    res = requests.get(url)
    return validated_response(res)


def get_user_results(handle):
    url = "atcoder-api/results"
    param = {'user': handle}
    res = requests.get(url, params=param)
    return validated_response(res)
