from django import test
from .test_setup import TestSetUp
from ..api import *


class Test(TestSetUp):

    def test_atcoder_get_all_contests(self):
        res = get_all_contests()
        self.assertEqual(res[0]["id"], "APG4b")

    def test_atcoder_get_all_problems(self):
        res = get_all_problems()
        self.assertEqual(res[0]["id"], "APG4b_a")

    def test_atcoder_get_all_problems_models(self):
        res = get_all_problems_models()
        self.assertEqual(res["abc138_a"]["difficulty"], -848)

    def test_atcoder_get_user_results(self):
        res = get_user_results('amann')
        self.assertEqual(res[0]["id"], 24029123)
