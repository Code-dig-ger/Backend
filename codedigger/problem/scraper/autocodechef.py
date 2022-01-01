import requests
from bs4 import BeautifulSoup
from time import sleep

import os, json, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codedigger.settings")
django.setup()

from problem.models import Problem

platform = "C"


def autoCodechefScrap(num=0):
    # This function is for scrapping all latest contest

    main_url = f"https://www.codechef.com/api/list/contests/past?sort_by=END&sorting_order=desc&offset={num}"
    r = requests.get(main_url)
    r = r.json()

    contests_code = []

    for cont in r['contests']:
        code = cont['contest_code']
        contests_code.append(code)

    # for long challenge contest code
    mon = [
        "JAN", "FEB", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUG", "SEPT",
        "OCT", "NOV", "DEC"
    ]
    # contests having A, B, C Category are longChallenge(MONXX), CookOffs(COOKXX), LunctTime(LTIMEXX), Starter(STARTXX)
    # problem_fetch_url = f"https://www.codechef.com/api/contests/{cont}"

    cont_url = "https://www.codechef.com/api/contests/"
    div = ['A', 'B', 'C']
    contest_tobe_scrapped = []

    for c in contests_code:
        code5 = c[:5]
        code4 = c[:4]
        code3 = c[:3]

        if (code5 in mon) or (code5 == 'LTIME') or (code5 == 'START'):
            contest_tobe_scrapped.append(c)
        elif (code4 in mon) or (code4 == 'COOK'):
            contest_tobe_scrapped.append(c)
        elif (code3 in mon):
            contest_tobe_scrapped.append(c)

    for c in contest_tobe_scrapped:
        for d in div:
            cont_res = requests.get(cont_url + c + d)
            sleep(1)
            if (cont_res.status_code != 200):
                continue

            data = cont_res.json()
            if data['status'] != "success":
                continue

            storeProb(data, c + d)


def storeProb(data, cont):

    b_url = "https://www.codechef.com"
    for item in data['problems']:

        if data['problems'][item]['category_name'] != 'main':
            continue

        n = data['problems'][item]['name']
        u = b_url + data['problems'][item]['problem_url']
        c = data['problems'][item]['code']
        p = Problem.objects.first()

        try:
            p = Problem.objects.get(prob_id=c, platform=platform)
        except Problem.DoesNotExist:
            p = None

        if p:
            contstr = p.contest_id
            contlist = contstr.split("-")
            # checks if contest already scrapped or not
            if cont in contlist:
                continue

            contlist.append(cont)
            contstr = "-".join(contlist)
            if contstr[0] == "-":
                contstr = contstr[1:]
            p.contest_id = contstr
            p.save()
        else:
            contlist = []
            contlist.append(cont)
            contstr = "-".join(contlist)
            if contstr[0] == "-":
                contstr = contstr[1:]
            p = Problem.objects.create(name=n,
                                       prob_id=c,
                                       url=u,
                                       contest_id=contstr,
                                       platform=platform)


def codechefProblem2021():
    # this function need to be called only once to store problems from jan21 to till date

    for i in range(20, 100, 20):
        autoCodechefScrap(num=i)
