import requests
from math import log2

from problem.models import Problem

from .utils import rating_to_difficulty
from .api import problem_list

def update_uva_problems():

    try : 
        data = problem_list()
    except : 
        return

    for p in data:

        if len(Problem.objects.filter(prob_id=p[0])) > 0:
            continue

        new_problem = Problem()
        new_problem.prob_id = p[0]
        new_problem.index = p[1]
        new_problem.name = p[2]
        dacu = p[3]
        wa = p[16]

        if dacu != 0:
            rating = min(3600, max(800, (20 - min(log2(dacu), 20)) * 200))
            new_problem.rating = str(int(rating))
            new_problem.difficulty = rating_to_difficulty(rating)

        new_problem.platform = 'U'
        new_problem.url = "https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=" + str(
            p[0])
        new_problem.save()

    url = "https://uhunt.onlinejudge.org/api/cpbook/3"
    res = requests.get(url)
    data = res.json()

    for p in data:
        title1 = p['title']
        for q in p['arr']:
            title2 = q['title']
            for r in q['arr']:
                title3 = r[0]
                for i in range(1, len(r)):
                    prob_num = abs(r[i])
                    tags = [title1, title2, title3]
                    Problem.objects.filter(index=prob_num).update(tags=tags)
