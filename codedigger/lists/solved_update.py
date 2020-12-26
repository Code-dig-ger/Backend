import requests
import bs4

import os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codedigger.settings")
django.setup()
from lists.models import Solved
from user.models import User
from problem.models import Problem


def codechef(user):
    url = 'https://www.codechef.com/users/'+user
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    problems_solved = soup.find('section' , {'class' : 'rating-data-section problems-solved'})
    if problems_solved.find('h5').text == 'Fully Solved (0)':
        pass
    for ele in problems_solved.find('article').find_all('a'):
        curr_user = User.objects.filter(username = user).first()
        prob = Problem.objects.filter(prob_id = ele.text).first()
        if not prob:
            continue
        qs = Solved.objects.filter(user=curr_user,problem=prob).first()
        if not qs:
            Solved.objects.create(user=curr_user,problem=prob)
        