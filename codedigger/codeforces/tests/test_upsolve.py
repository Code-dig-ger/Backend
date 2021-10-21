from django import test
from .test_setup import TestSetUp
from django.urls import reverse


class TestUpsolve(TestSetUp):
    def test_codeforces_upsolve(self):
        test_url = reverse('cf_upsolve')
        token = self.login(self.client, self.login_url, self.user_data)
        client = self.get_authenticated_client(token)
        res = client.get(test_url, format="json")
        self.assertEqual(res.data['meta']['total'], 1)
        self.assertEqual(len(res.data['result']), res.data['meta']['to'])

    def test_codeforces_virtual_upsolve(self):
        test_url = reverse('cf_upsolve') + '?virtual=true'
        token = self.login(self.client, self.login_url, self.user_data)
        client = self.get_authenticated_client(token)
        res = client.get(test_url, format="json")
        self.assertEqual(res.data['meta']['total'], 2)
        self.assertEqual(len(res.data['result']), res.data['meta']['to'])

    def test_codeforces_without_auth_upsolve(self):
        test_url = reverse('cf_upsolve') + '?handle=aaradhya0707'
        res = self.client.get(test_url, format="json")
        self.assertEqual(res.data['meta']['total'], 1)
        self.assertEqual(len(res.data['result']), res.data['meta']['to'])
