# from django.test import TestCase
from .test_setup import TestSetUp
from codeforces.contestProblem import AssignCodeforcesProblem
from codeforces.models import user


class Test_assign_problem(TestSetUp):

    def test_Assign(self):
        test_user = user.objects.get(handle='tourist')
        problems = AssignCodeforcesProblem(test_user)
        self.assertEqual(len(problems), 5)
