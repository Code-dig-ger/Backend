import requests
from bs4 import BeautifulSoup


def problem_page(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html5lib')
    return soup
