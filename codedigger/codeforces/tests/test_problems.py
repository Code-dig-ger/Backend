# from django.test import TestCase
from .test_setup import TestSetUp
from codeforces.contestProblem import CodeforcesAssignProblem
from codeforces.test_fixtures.models_utils_fixture import cf_user


class Test_assign_problem(TestSetUp):
    def test_Assign(self):
        self.assertEqual((CodeforcesAssignProblem(cf_user)), [])
