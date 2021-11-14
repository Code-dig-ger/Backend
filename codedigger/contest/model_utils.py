from .models import CodeforcesContest, CodeforcesContestProblem

def get_user_contests(user):
    return CodeforcesContest.objects.filter(owner = user)\
                                    .order_by('-startTime')

def get_contest_problem(contest):
    return CodeforcesContestProblem.objects\
                                .filter(codeforcesContest= contest)\
                                .values_list('problem', flat = True) 