from datetime import datetime
from problem.models import Problem
from codechef.models import CodechefContest, CodechefContestProblems
from codechef.scraper_utils import ContestData, ProblemData


def create_or_update_codechefProblem(contestId):
    problemdata = ProblemData(contestId)
    for problem in problemdata:
        Prob, created = Problem.objects.get_or_create(name=problem['Name'],
                                     prob_id=problem['ProblemCode'],
                                     url=problem['ProblemURL'],
                                     contest_id=contestId,
                                     platform=problem['Platform'])
        # Prob.name = problem['Name']
        # Prob.url = problem['ProblemURL']
        # Prob.contest_id = contestId
        cont = CodechefContest.objects.get(contestId=problem['ContestId'])
        codechefProb = CodechefContestProblems.objects.get_or_create(contest = cont, problem = Prob)


def create_or_update_codechefContest(contest):
        contestDate = datetime.strptime(contest['StartTime'],
                                        "%d %B %Y  %H:%M:%S")
        cont = CodechefContest.objects.get_or_create(
            name=contest['Name'],
            contestId=contest['ContestCode'],
            duration=contest['Duration'],
            startTime=contestDate,
            url=contest['ContestURL'])

        
