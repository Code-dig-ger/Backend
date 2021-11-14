from django.core.checks.messages import Error
from utils.email import send_error_mail, send_testing_mail
from utils.common import rating_to_difficulty

from problem.models import Problem

from .model_utils import create_or_update_contest, create_or_update_problem
from .api import (get_all_contests, get_all_problems, get_all_problems_models)


def update_atcoder():
    send_testing_mail('Atcoder Problem Update Process Started')
    
    try:
        data = get_all_contests()
    except Exception as e:
        send_error_mail('Atcoder Problem Update Kenkoo API All Contests Error',e)
        return
    
    for contest in data:
        create_or_update_contest(contest)

    try:
        data = get_all_problems()
    except Exception as e:
        send_error_mail('Atcoder Problem Update Kenkoo API All Problems Error',e)
        return

    for prob in data:
        create_or_update_problem(prob)

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

    send_testing_mail('Atcoder Problem Update Process Finished')