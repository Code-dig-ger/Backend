import requests
from math import log2
from problem.models import Problem, atcoder_contest
from .api import * 
from utils.common import rating_to_difficulty


def update_atcoder_problems():
    data = get_all_contests()

    for contest in data:

        if len(atcoder_contest.objects.filter(contestId=contest['id'])) == 0:

            new_contest = atcoder_contest()
            new_contest.name = contest['title']
            new_contest.contestId = contest['id']
            new_contest.startTime = contest['start_epoch_second']
            new_contest.duration = contest['duration_second']
            new_contest.save()

    data = get_all_problems()

    for prob in data:

        if len(Problem.objects.filter(prob_id=prob['id'], platform='A')) == 0:

            new_problem = Problem()
            new_problem.prob_id = prob['id']
            new_problem.contest_id = prob['contest_id']
            new_problem.name = prob['title']
            new_problem.url = "https://atcoder.jp/contests/" + prob[
                'contest_id'] + "/tasks/" + prob['id']
            new_problem.index = prob['id'].split("_")[-1]
            new_problem.platform = 'A'
            new_problem.save()

    data = get_all_problems_models()

    problems = Problem.objects.filter(difficulty=None, platform='A')

    for prob in problems:

        if prob.prob_id in data:

            if 'difficulty' in data[prob.prob_id]:

                old = data[prob.prob_id]['difficulty']
                if old < -1000:
                    NewValue = (((old + 10000) * 50) / 9000) + 800
                elif old <= 0:
                    NewValue = (((old + 1000) * 350) / 1000) + 850
                else:
                    NewValue = ((old * 2400) / 5000) + 1200

                prob.rating = str(int(NewValue))
                prob.difficulty = rating_to_difficulty(int(NewValue))
                prob.save()
