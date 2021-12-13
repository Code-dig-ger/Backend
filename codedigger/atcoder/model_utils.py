from problem.models import Problem
from .models import atcoder_contest


def create_or_update_contest(contest):
    new_contest = atcoder_contest.get_or_create(
        id=contest['id'],
        defaults={
            'name': contest['title'],
            'startTime': contest['start_epoch_second'],
            'duration': contest['duration_second']
        })
    new_contest.save()


def create_or_update_problem(problem):
    new_problem = Problem.get_or_create(
        prob_id=problem['id'],
        platform='A',
        defaults={
            'name':
            problem['title'],
            'contest_id':
            problem['contest_id'],
            'url':
            "https://atcoder.jp/contests/{}/tasks/{}".format(
                problem['contest_id'], problem['id']),
            'index':
            problem['id'].split("_")[-1]
        })
    new_problem.save()