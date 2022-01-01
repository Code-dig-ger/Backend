# Models
from .models import CodeforcesContest, CodeforcesContestProblem
from problem.models import Problem


def get_user_contests(user):
    return CodeforcesContest.objects.filter(owner = user)\
                                    .order_by('-startTime')


def get_contest_problem(contest):
    return CodeforcesContestProblem.objects\
                                .filter(codeforcesContest= contest)\
                                .order_by('index')\
                                .values_list('problem', flat = True)


def get_contest_problem_qs(contest):
    contest_problem_ids = get_contest_problem(contest)
    contest_problem_qs = []
    for id in contest_problem_ids:
        contest_problem_qs.append(Problem.objects.get(id=id))
    return contest_problem_qs


def put_contest_problem(contest, problems):
    for idx, problem in enumerate(problems):
        CodeforcesContestProblem(codeforcesContest=contest,
                                 problem=problem,
                                 index=idx).save()
