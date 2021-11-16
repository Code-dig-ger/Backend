from .test_setup import TestSetUp
from codeforces.scraper_utils import isSameProblem


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