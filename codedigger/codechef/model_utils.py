from .models import CodechefContest
from .models import CodechefContest, CodechefContestProblems
from problem.models import Problem
from codechef.scraper import contestScraper, problemScraper, divisionScraper
from codechef.scraper_utils import OffsetLoader, getContestDivision, ContestData, ProblemData


def create_or_update_codechefContest():
    all_contests = ContestData()

    for contest in all_contests:
        cont = CodechefContest.objects.get_or_create(
            name=contest['Name'],
            contestId=contest['ContestCode'],
            duration=contest['Duration'])
