import requests
from bs4 import BeautifulSoup
from time import sleep

import os, json, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codedigger.settings")
django.setup()
from problem.models import Problem
from codechef.models import CodechefContest, CodechefContestProblems

platform = "C"


def tagsScraper():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'taglist.txt')
    with open(file_path, 'r') as f:
        for line in f:

            t = line[:-1]

            url = f"https://www.codechef.com/get/tags/problems/{t}"
            r = requests.get(url)

            if r.status_code != 200:
                continue

            data = r.json()
            # data = {}

            # dataform = str(r).strip("'<>() ").replace('\'', '\"')
            # data = json.loads(dataform)

            b_url = "https://www.codechef.com/problems/"

            for item in data['all_problems']:
                prob_id = data['all_problems'][item]['code']
                tag = data['all_problems'][item]['tags']
                title = prob_id
                link = b_url + prob_id
                try:
                    pro = Problem.objects.get(prob_id=prob_id,
                                              platform=platform)
                except Problem.DoesNotExist:
                    pro = None

                if pro:
                    pro.tags = tag
                    pro.save()
                else:
                    Problem.objects.create(name=title,
                                           prob_id=prob_id,
                                           url=link,
                                           tags=tag,
                                           platform=platform)


def longChallenge(b_url, div, mon, yr):
    #print("longchallenge started")

    for y in yr:
        for m in mon:
            for d in div:
                # driver.get(url+m+y+d)
                if y == "18" and (m == "JAN" or m == "FEB"):
                    if (d == "B"):
                        break
                    cont = m + y
                else:
                    cont = m + y + d
                    # driver.get(b_url+cont)

                url = f"https://www.codechef.com/api/contests/{cont}?v=1608807222132"
                r = requests.get(url)
                if r.status_code != 200:
                    continue
                data = r.json()
                storeProb(data, cont, b_url)


def lunchTime(b_url, div):
    #print("lunch time started")
    latestLunch = 90
    while latestLunch > 57:
        for d in div:
            cont = "LTIME" + str(latestLunch) + d
            url = f"https://www.codechef.com/api/contests/{cont}?v=1608807222132"
            r = requests.get(url)
            if r.status_code != 200:
                continue
            data = r.json()
            storeProb(data, cont, b_url)
        latestLunch = latestLunch - 1


def cookOff(b_url, div):
    #print("cookOFF started")
    latestOff = 125
    while latestOff > 91:
        for d in div:
            cont = "COOK" + str(latestOff) + d
            url = f"https://www.codechef.com/api/contests/{cont}?v=1608807222132"
            r = requests.get(url)
            if r.status_code != 200:
                continue
            data = r.json()
            storeProb(data, cont, b_url)
        latestOff = latestOff - 1


def storeProb(data, cont, b_url):
    for item in data['problems']:

        if data['problems'][item]['category_name'] != 'main':
            continue

        n = data['problems'][item]['name']
        u = b_url + data['problems'][item]['problem_url']
        c = data['problems'][item]['code']

        try:
            p = Problem.objects.get(prob_id=c, platform=platform)
        except Problem.DoesNotExist:
            p = None

        if (not p):
            if cont[-1] == "B":
                Problem.objects.create(name=n,
                                       prob_id=c,
                                       url=u,
                                       index=cont,
                                       platform=platform)
            else:
                Problem.objects.create(name=n,
                                       prob_id=c,
                                       url=u,
                                       contest_id=cont,
                                       platform=platform)
        else:
            if cont[-1] == "B":
                p.index = cont
                p.save()
            else:
                p.contest_id = cont
                p.save()

        cont = CodechefContest.objects.create(contestId=cont)
        CodechefContestProblems.objects.create(contest=cont, problem=p)


def contestIdScraper():
    div = ["A", "B"]
    yr = ["18", "19", "20"]
    mon = [
        "JAN", "FEB", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUG", "SEPT",
        "OCT", "NOV", "DEC"
    ]
    b_url = "https://www.codechef.com"
    longChallenge(b_url, div, mon, yr)
    lunchTime(b_url, div)
    cookOff(b_url, div)


def codeChefScraper():
    levels = [
        "school/", "easy/", "medium/", "hard/", "challenge/", "extcontest/"
    ]
    f_url = "https://www.codechef.com/problems/"
    b_url = "https://www.codechef.com"

    # Acessing each level page

    for level in levels:
        # requesting site for data
        r = requests.get(f_url + level)
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.content, 'html5lib')
        problemRow = soup.findAll('tr', class_="problemrow")
        for pr in problemRow:
            data = pr.findAll('td')
            if level == 'school/':
                difficulty = "B"
            elif level == 'extcontest/':
                difficulty = ""
            else:
                difficulty = level[0].upper()

            url = b_url + data[0].find('a').get('href')
            name = data[0].text.replace("  ", "").replace('\n', "")
            prob_id = data[1].text
            index = ""
            contest_id = ""
            tags = []
            try:
                p = Problem.objects.get(prob_id=prob_id, platform=platform)
            except Problem.DoesNotExist:
                p = None
            if (not p):
                Problem.objects.create(name=name,
                                       prob_id=prob_id,
                                       url=url,
                                       tags=tags,
                                       contest_id=contest_id,
                                       platform=platform,
                                       index=index,
                                       difficulty=difficulty)
    tagsScraper()
    contestIdScraper()
