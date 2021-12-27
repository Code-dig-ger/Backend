# from django.test import TestCase
from .test_setup import TestSetUp
from codeforces.contestProblem import AssignCodeforcesProblem
from codeforces.models import user
from codeforces.api import contest_submissions


class Test_assign_problem(TestSetUp):

    def test_Assign(self):
        test_user = user.objects.get(handle='tourist')
        problems = AssignCodeforcesProblem(test_user)
        self.assertEqual(len(problems), 5)

    def test_contestSubmissions(self):
        submissions=contest_submissions(contestId=1619,handle='surya7240')
        submissions2=contest_submissions(contestId=1619,count=50)
        submissions3=contest_submissions(contestId=1619)
        self.assertEqual(len(submissions), 2)
        self.assertEqual(len(submissions2), 50)
        self.assertEqual(len(submissions3), 1000)