from .test_setup import TestSetUp
from codechef.models import CodechefContest, CodechefContestProblems
from problem.models import Problem
from codechef.model_utils import create_or_update_codechefContest,create_or_update_codechefProblem
from codechef.test_fixtures.model_utils_fixture import (codechef_contest,codechef_problem)
from datetime import datetime

class TestModelUtils(TestSetUp):
    def test_CreateContest(self):
        newContest = create_or_update_codechefContest(codechef_contest)
        contestDate = datetime.strptime(codechef_contest["StartTime"],"%d %B %Y  %H:%M:%S")
        contest = CodechefContest.objects.get(contestId = codechef_contest["ContestCode"])
        self.assertEqual(contest.url, codechef_contest["ContestURL"])
        self.assertEqual(contest.contestId, 'COOK117B')


    def test_CreateProblem(self):
        create_or_update_codechefContest(codechef_contest)
        create_or_update_codechefProblem(codechef_problem)
        problemModel = Problem.objects.get(prob_id = codechef_problem[0]['ProblemCode'])
        firstProbCode = codechef_problem[0]['ProblemCode']
        codechefProblem = CodechefContestProblems.objects.filter(problem = problemModel)
        self.assertEqual(codechefProblem[0].problem.prob_id, 'LIFTME')