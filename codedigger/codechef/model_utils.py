from datetime import datetime
from problem.models import Problem
from codechef.models import CodechefContest, CodechefContestProblems


def create_or_update_codechefProblem(problemdata):
    for problem in problemdata:
        Prob, created = Problem.objects.get_or_create(
            name=problem['Name'],
            prob_id=problem['ProblemCode'],
            url=problem['ProblemURL'],
            contest_id=problem['ContestId'],
            platform=problem['Platform'])
        cont = CodechefContest.objects.get(contestId=problem['ContestId'])
        prob = Problem.objects.get(prob_id=problem['ProblemCode'],
                                   contest_id=problem['ContestId'])
        ccprob, created = CodechefContestProblems.objects.get_or_create(
            contest=cont, problem=prob)


def create_or_update_codechefContest(contest):
    contestDate = datetime.strptime(contest['StartTime'], "%d %B %Y  %H:%M:%S")
    cont = CodechefContest.objects.get_or_create(
        name=contest['Name'],
        contestId=contest['ContestCode'],
        duration=contest['Duration'],
        startTime=contestDate,
        url=contest['ContestURL'])

    # create_or_update_codechefProblem(contest_problems_info)
