from datetime import datetime

from .models import CodechefContest
from .models import CodechefContest, CodechefContestProblems
from problem.models import Problem
from codechef.scraper import contestScraper, problemScraper, divisionScraper
from codechef.scraper_utils import OffsetLoader, getContestDivision, ContestData, ProblemData


def create_or_update_codechefProblem(problemdata):
    for problem in problemdata:
        Prob = Problem.get_or_create(name=problem['Name'],
                                     prob_id=problem['ProblemCode'],
                                     url=problem['ProblemURL'],
                                     contest_id=problem['ContestId'],
                                     platform=problem['Platform'])
        cont = CodechefContest.objects.get_or_create(
            contestId=Problem['ContestCode'], )
        codechefProb = CodechefContestProblems.get_or_create(contest=cont,
                                                             problem=Prob)


def create_or_update_codechefContest():
    all_contests = ContestData()

    for contest in all_contests:

        contestDate = datetime.strptime(contest['contest_start_date'],
                                        "%d %B %Y  %H:%M:%S")
        cont = CodechefContest.objects.get_or_create(
            name=contest['Name'],
            contestId=contest['ContestCode'],
            duration=contest['Duration'],
            StartTime=contestDate,
            url=contest['ContestURL'])

        contest_problems_info = ProblemData(contestId)
        create_or_update_codechefProblem(contest_problems_info)
