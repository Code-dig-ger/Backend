from .test_setup import TestSetUp
from codechef.scraper import problemScraper
from codechef.scraper_utils import getContestDivision, ProblemData
from codechef.test_fixtures.scraper_utils_fixture import (problemResult,
                                                          contestResult,
                                                          getDivisionResult1,
                                                          getDivisionResult2)


class TestScraper(TestSetUp):

    def test_problemScraper(self):

        code = "APRIL19B"

        output_result = problemScraper(code)
        self.assertEqual("status" in output_result, True,
                         "Couldn't fetch status result in problemScraper")
        self.assertEqual(output_result["status"], "success",
                         "Failed status in problemScraper")
        self.assertEqual("code" in output_result, True,
                         "problemScraper doesn't contain the contest code")
        self.assertEqual("problems" in output_result, True,
                         "problemScraper doesn't have the problem info")

    def test_ProblemData(self):
        code = "COOK130B"

        problems_all = ProblemData(code)
        self.assertTrue(len(problems_all) >= 1)
        self.assertEqual(problemResult, problems_all)

    def test_getDivisionInfo(self):
        code1 = "COOK129"
        code2 = "LTIME15"

        output1 = getContestDivision(code1)
        output2 = getContestDivision(code2)

        self.assertEqual(output1, getDivisionResult1,
                         "Incorrect Division Details for test 1!")
        self.assertEqual(output2, getDivisionResult2,
                         "Incorrect Division Details for test 2!")
