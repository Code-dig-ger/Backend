from problem.models import Problem
from codechef.models import CodechefContest,CodechefContestProblems
from codechef.scraper import contestScraper,problemScraper,divisionScraper
from codechef.scraper_utils import ContestData,ProblemData,getContestDivision,OffsetLoader
from codechef.model_utils import create_or_update_codechefContest,create_or_update_codechefProblem


def update_AllContests():
    # Creates new contests and problems in Database
    all_contests = ContestData()
    for contest in all_contests:
        create_or_update_codechefContest(contest)
        contestId = contest['ContestCode']
        create_or_update_codechefProblem(contestId)
        
        