from django import test
from .test_setup import TestSetUp
from django.urls import reverse


class TestUpsolve(TestSetUp):

    def test_codechef_upsolve(self):
        test_url = reverse('codechef-upsolve')
        token = self.login(self.client, self.login_url, self.user_data)
        client = self.get_authenticated_client(token)
        res = client.get(test_url, format="json")
        self.assertEqual(len(res.data['result'][0]['problems']), 5)
        self.assertEqual(res.data['meta']['total'], 3)
        self.assertEqual(len(res.data['result']), res.data['meta']['to'])
