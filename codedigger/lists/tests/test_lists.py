from django.test import client

from user.exception import ValidationException
from .test_setup import TestSetUp
from user.models import User, Profile
from django.urls import reverse
from rest_framework.test import APIClient


class TestViews(TestSetUp):
    def test_check_owner_can_change_visibility_view(self):
        slug = "testinglist_userlist"
        test_url = reverse('userlist-edit', kwargs={'slug': slug})
        here = User.objects.get(username="testing")
        here.set_password(self.user_data['password'])
        here.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        token = res.data['tokens']['access']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = client.put(test_url, {'public': True}, format="json")
        user = User.objects.get(username="testinguser")
        user.set_password(self.user_data['password'])
        user.save()
        res2 = self.client.post(self.login_url, {
            'username': 'testinguser',
            'password': self.user_data['password']
        },
                                format="json")
        token2 = res2.data['tokens']['access']
        client2 = APIClient()
        client2.credentials(HTTP_AUTHORIZATION='Bearer ' + token2)
        res2 = client2.put(test_url, {'public': True}, format="json")
        self.assertEqual(res.status_code, 200) and self.assertEqual(
            res2.status_code, 400)

    def test_check_restrict_change_visibility_view(self):
        slug = "testinglist_userlist"
        test_url = reverse('userlist-edit', kwargs={'slug': slug})
        here = User.objects.get(username="testing")
        here.set_password(self.user_data['password'])
        here.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        token = res.data['tokens']['access']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = client.put(test_url, {'public': True}, format="json")
        res2 = client.put(test_url, {'public': False}, format="json")
        self.assertEqual(res.status_code, 200) and self.assertEqual(
            res2.status_code, 400)

    def test_check_only_owner_can_add_problems_view(self):
        test_url = reverse('userlist-add')
        here = User.objects.get(username="testing")
        here.set_password(self.user_data['password'])
        here.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        token = res.data['tokens']['access']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data1 = {
            'prob_id': "4A",
            'slug': 'testinglist_userlist',
            'platform': 'F'
        }
        res = client.post(test_url, data1, format="json")
        user = User.objects.get(username="testinguser")
        user.set_password(self.user_data['password'])
        user.save()
        res2 = self.client.post(self.login_url, {
            'username': 'testinguser',
            'password': self.user_data['password']
        },
                                format="json")
        token2 = res2.data['tokens']['access']
        client2 = APIClient()
        client2.credentials(HTTP_AUTHORIZATION='Bearer ' + token2)
        data2 = {
            'prob_id': "abc186_a",
            'slug': 'testinglist_userlist',
            'platform': 'A'
        }
        res2 = client2.post(test_url, data2, format="json")
        self.assertEqual(res.status_code, 200) and self.assertEqual(
            res2.status_code, 400)

    def test_get_user_list(self):
        username = "testing"
        test_url = reverse('user-list',kwargs={'username': username})
        here = User.objects.get(username="testing")
        here.set_password(self.user_data['password'])
        here.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        token = res.data['tokens']['access']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = client.get(test_url, format="json")
        
        username2 = "testing1"
        test_url = reverse('user-list',kwargs={'username': username2})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res2 = client.get(test_url, format="json")

        self.assertEqual(res.status_code, 200) and self.assertRaises(ValidationException, res2)
        if(len(res.data['result'])>0):
            self.assertEqual(res.data['result'][0]['public'],True)

    def test_get_stats(self):
        slug = "testinglist_levelwise"
        test_url = reverse('user-standing', kwargs={'slug': slug})
        token = self.login(self.client, self.login_url, self.user_data)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = client.get(test_url, format="json")
        
        slug = "testinglist_userlist"
        token = self.login(self.client, self.login_url, self.user_data)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res2 = client.get(test_url, format="json")

        self.assertEqual(res.status_code, 200) and self.assertRaises(ValidationException, res2)

    def test_get_friends_stats(self):
        slug = "testinglist_levelwise"
        test_url = reverse('friends-standing', kwargs={'slug': slug})
        here = User.objects.get(username="testing")
        here.set_password(self.user_data['password'])
        here.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        token = res.data['tokens']['access']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = client.get(test_url, format="json")

        self.assertEqual(res.status_code, 200)