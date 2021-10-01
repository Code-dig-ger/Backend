from .test_setup import TestSetUp
from user.models import User, Profile
from django.urls import reverse
from rest_framework.test import APIClient
from lists.models import List, ListInfo, Solved
from problem.models import Problem


class TestViews(TestSetUp):

    #anon checking of list of all ladders and list endpoints
    def test_check_topicwise_list_all_lists_view(self):
        test_url = reverse('topicwise-list')
        res = self.client.get(test_url)
        self.assertEqual(res.status_code, 200)

    def test_check_topicwise_ladder_all_ladders_view(self):
        test_url = reverse('topicwise-ladder')
        res = self.client.get(test_url)
        self.assertEqual(res.status_code, 200)

    def test_check_levelwise_list_all_lists_view(self):
        test_url = reverse('levelwise-list')
        res = self.client.get(test_url)
        self.assertEqual(res.status_code, 200)

    def test_check_levelwise_ladder_all_ladder_view(self):
        test_url = reverse('levelwise-ladder')
        res = self.client.get(test_url)
        self.assertEqual(res.status_code, 200)

#same as above but with an authenticated user

    def test_auth_check_topicwise_list_all_lists_view(self):
        test_url = "http://127.0.0.1:8000/lists/topicwise/list/testinglist_topicwise"
        here = User.objects.get(username="testing")
        here.set_password(self.user_data['password'])
        here.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        token = res.data['tokens']['access']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = client.get(test_url, format="json")
        self.assertEqual(res.status_code, 200)
