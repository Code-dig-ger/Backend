from .test_setup import TestSetUp
from django.urls import reverse


class TestViews(TestSetUp):

    def test_search_user(self):
        url = reverse('search-user')
        url += '?q=tou'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(max(len(response.data['result']), 5), 5)
        users = response.data['result']
        for i in users:
            handle = i['handle'].lower()
            self.assertEqual('tou', handle[:3])
