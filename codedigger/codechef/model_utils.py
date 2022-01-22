from datetime import datetime
from problem.models import Problem
from codechef.models import CodechefContest, CodechefContestProblems


def create_or_update_codechefProblem(problemdata):
    for problem in problemdata:
        Prob, created = Problem.objects.get_or_create(
            prob_id=problem['ProblemCode'],
            platform=problem['Platform'],
            defaults={
                'name': problem['Name'],
                'url': problem['ProblemURL'],
                'contest_id': problem['ContestId'],
            },
        )

        cont = CodechefContest.objects.get(contestId=problem['ContestId'])

        ccprob, created = CodechefContestProblems.objects.get_or_create(
            contest=cont, problem=Prob)


def create_or_update_codechefContest(contest):
    contestDate = datetime.strptime(contest['StartTime'], "%d %B %Y  %H:%M:%S")
    cont = CodechefContest.objects.get_or_create(
        name=contest['Name'],
        contestId=contest['ContestCode'],
        duration=contest['Duration'],
        startTime=contestDate,
        url=contest['ContestURL'])

    # create_or_update_codechefProblem(contest_problems_info)
