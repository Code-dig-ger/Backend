import requests

def get_user_history(handle):
    url = "https://atcoder.jp/users/" + handle + "/history"
    res = requests.get(url)
    return res