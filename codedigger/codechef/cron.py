from .model_utils import create_or_update_codechefContest,create_or_update_codechefProblem
from .models import CodechefContest,CodechefContestProblems
from problem.models import Problem
from .scraper_utils import ContestData,ProblemData,getContestDivision
from .scraper import contestScraper,problemScraper,divisionScraper


def OffsetLoader(contest_type):

    requested_contests = []
    for i in range(0, 60, 20):  #offset {0, 20, 40} for multiple pages of contests.
        contests_data = contestScraper(i, contest_type)

        for contests in contests_data['contests']:
            requested_contests.append(contests)

    return requested_contests


def update_AllContests():
    # Creates new contests and problems in Database
    all_contests = ContestData()
    for contest in all_contests:
        create_or_update_codechefContest(contest)
        contestId = contest['ContestCode']
        create_or_update_codechefProblem(contestId)
        
        