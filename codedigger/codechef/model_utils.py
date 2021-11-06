from datetime import datetime
from problem.models import Problem
from codechef.models import CodechefContest, CodechefContestProblems
from codechef.scraper_utils import ContestData, ProblemData


def create_or_update_codechefProblem(contestId):
    problemdata = ProblemData(contestId)
    cont = CodechefContest.objects.get(contestId=contestId)

    for problem in problemdata:
        Prob, created = Problem.objects.get_or_create(prob_id=problem['ProblemCode'])
        Prob.name=problem['Name']
        Prob.url=problem['ProblemURL']
        Prob.contest_id=contestId
        Prob.platform=problem['Platform']
        CodechefContestProblems.objects.get_or_create(contest = cont, problem = Prob)


def create_or_update_codechefContest(contest):
        contestDate = datetime.strptime(contest['StartTime'],
                                        "%d %B %Y  %H:%M:%S")
        CodechefContest.objects.get_or_create(
            contestId=contest['ContestCode'],
            defaults={
                'name': contest['Name'],
                'duration': contest['Duration'],
                'startTime': contestDate,
                'url': contest['ContestURL']
            })

        
