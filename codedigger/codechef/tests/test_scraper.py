from .test_setup import TestSetUp
from codechef.scraper import ContestProblemScraper


class TestScraper(TestSetUp):
    def test_contestProblemScraper(self):
        code = "APRIL19B"
        result = {}
        res = ContestProblemScraper(code)
