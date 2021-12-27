from .models import contest
from problem.models import Problem
from .api import user_status
from .api_utils import get_all_submission


def AssignCodeforcesProblem(cf_user):

    # Set Minimum rating as 1000 and maximum rating as 2500
    userRating = cf_user.rating // 100 * 100
    userRating = min(max(userRating, 1000), 2500)

    contests = contest.objects.filter(Type__exact='R')
    contestIds = [contest.contestId for contest in contests]

    problems = Problem.objects.filter(contest_id__in=contestIds,
                                      platform='F',
                                      difficulty__isnull=False,
                                      rating__gte=userRating - 200,
                                      rating__lte=userRating + 200)

    # Excluding all the submissions that have seen by the user
    submissions = user_status(cf_user.handle)
    probIds = get_all_submission(submissions)
    problems = problems.exclude(prob_id__in=probIds)

    # Assigning the problem as per the order
    # rating-200,rating-100,=rating,rating+100,rating+200
    AssignedProblem = []
    userRating -= 200
    for i in range(5):
        for problem in problems:
            if problem.rating == userRating:
                AssignedProblem.append(problem)
                break
        userRating += 100

    return AssignedProblem
