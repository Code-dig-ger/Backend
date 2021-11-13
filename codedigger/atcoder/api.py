import requests


def get_all_contests():
    url = "https://kenkoooo.com/atcoder/resources/contests.json"
    res = requests.get(url)
    data = res.json()
    return data


def get_all_problems():
    url = "https://kenkoooo.com/atcoder/resources/problems.json"
    res = requests.get(url)
    data = res.json()
    return data


def get_all_problems_models():
    url = "https://kenkoooo.com/atcoder/resources/problem-models.json"
    res = requests.get(url)
    data = res.json()
    return data


def get_user_history(handle):
    url = "https://atcoder.jp/users/" + handle + "/history"
    res = requests.get(url)
    return res


def get_user_results(handle):
    url = "https://kenkoooo.com/atcoder/atcoder-api/results?user=" + handle
    res = requests.get(url)
    return res
