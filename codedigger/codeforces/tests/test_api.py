from .test_setup import TestSetUp
from codeforces.api import (user_info, contest_list, 
                            contest_standings, contest_ratingChanges)

class TestAPI(TestSetUp):

    def test_user_info_api(self):
        handles = ['shivamsinghal1012', 'shivam011']
        response = user_info(handles)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]['handle'], 'shivamsinghal1012')
    
    def test_contest_list(self):
        response = contest_list()
        self.assertLess(response[0]['id'], 100001)
        response = contest_list(gym=True)
        self.assertGreaterEqual(response[0]['id'], 100001)

    def test_contest_standings(self):
        response = contest_standings(566, count = 5)
        self.assertEqual(response['contest']['id'], 566)
        self.assertEqual(len(response['problems']), 7)
        self.assertEqual(len(response['rows']), 5)
        self.assertEqual(response['rows'][0]['party']['participantType'], 'CONTESTANT')
    
    def test_contest_ratingChanges(self):
        response = contest_ratingChanges(566)
        self.assertEqual(response[0]['rank'], 1)
