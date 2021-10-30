from .test_setup import TestSetUp
from .models import CodechefContest, CodechefContestProblems
from problem.models import Problem
from codechef.model_utils import create_or_update_codechefContest,create_or_update_codechefProblem
from codechef.test_fixtures.model_utils_fixture import (codechef_contest,codechef_problem)

class TestModelUtils(self):
    def test_CreateContest(self):
        newContest = create_or_update_codechefContest(codechef_contest)
        contest = CodechefContest.objects.filter(contestId = codechef_contest['ContestCode'])
        self.assertEqual(contest.exists(), True)
        self.assertEqual(contest.url, codechef_contest['ContestURL'])
        self.assertEqual(contest.startTime, codechef_contest['StartTime'])


    def test_CreateProblem(self):
        newProblem = create_or_update_codechefProblem(codechef_problem)
        firstProb = codechef_problem[0]
        problem = CodechefContest.objects.filter(contestId = firstProb['ContestId'])
        self.assertEqual(problem.exists(), True)
        self.assertEqual(len(problem),len(codechef_problem))