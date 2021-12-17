from django import test
from .test_setup import TestSetUp
from ..scrapers import  get_user_history

class Test(TestSetUp):
    def test_atcoder_scraper(self):
        res1 = get_user_history('amann')
        res2 = get_user_history('ewqe1e102931ndsmahwn1e1e')
        self.assertEqual(res1.status_code,200)
        self.assertEqual(res2.status_code,404)