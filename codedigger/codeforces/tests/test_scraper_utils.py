from .test_setup import TestSetUp

from problem.models import Problem
from codeforces.scraper_utils import isSameProblem
from codeforces.codeforcesProblemSet import join, get_similar_problems


class TestViews(TestSetUp):
    def test_is_same_problem(self):
        url1 = "https://codeforces.com/problemset/problem/1355/B"
        url2 = "https://codeforces.com/gym/102599/problem/D"
        self.assertTrue(isSameProblem(url1, url2))

        url1 = "https://codeforces.com/contest/1603/problem/A"
        url2 = "https://codeforces.com/contest/1604/problem/C"
        self.assertTrue(isSameProblem(url1, url2))

        url1 = "https://codeforces.com/contest/1603/problem/B"
        self.assertFalse(isSameProblem(url1, url2))
    
    def test_join_problem(self):
        probA = Problem.objects.get(prob_id = '100001A')
        probC = Problem.objects.get(prob_id = '1549C')
        probD = Problem.objects.get(prob_id = '1549D')
        probE = Problem.objects.get(prob_id = '1549E')

        join(probA, probC)
        join(probD, probE)
        join(probA, probE)

        self.assertEqual(get_similar_problems(probC).count(), 3)
