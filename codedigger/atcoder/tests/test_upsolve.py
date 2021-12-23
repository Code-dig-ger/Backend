from django import test
from .test_setup import TestSetUp
from django.urls import reverse


class TestUpsolve(TestSetUp):
    def test_atcoder_upsolve(self):
        test_url = reverse('at_upsolve') + '?practice=true'
        token = self.login(self.client, self.login_url, self.user_data)
        client = self.get_authenticated_client(token)
        res = client.get(test_url, format="json")
        self.assertEqual(len(res.data['result'][0]['problems']), 5)
        self.assertEqual(res.data['meta']['total'], 1)
        self.assertEqual(len(res.data['result']), res.data['meta']['to'])

    def test_atcoder_without_auth_upsolve(self):
        test_url = reverse('at_upsolve') + '?practice=true&handle=aaradhya0707'
        res = self.client.get(test_url, format="json")
        self.assertEqual(len(res.data['result'][0]['problems']), 5)
        self.assertEqual(res.data['meta']['total'], 1)
        self.assertEqual(len(res.data['result']), res.data['meta']['to'])
    
    def test_atcoder_without_auth_upsolve_wrong_handle(self):
        test_url = reverse('at_upsolve') + '?practice=true&handle=aaradhya070707'
        res = self.client.get(test_url, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data['error'], 'User not found in Atcoder')
