import re
import json
import requests
from bs4 import BeautifulSoup as bs4


def get_all_contests_details(content):
    contests_details = set()
    soup = bs4(content, 'html5lib')
    contestTable = soup.find('table', {'id': 'history'})
    del soup
    if contestTable != None:
        contests = contestTable.find('tbody').findAll('tr')
        del contestTable
        for contest in contests:
            contests_details.add(
                contest.findAll('td')[1].find('a')['href'].split('/')[-1])
        del contests
    return contests_details