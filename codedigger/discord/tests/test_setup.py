from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse

from user.models import User, Profile
from lists.test_fixtures.profile_fixtures import profile1


class TestSetUp(APITestCase):
    fixtures = ["user.json", "bot.json"]

    @classmethod
    def setUpTestData(cls):
        Profile.objects.filter(owner=1).update(**profile1)

    def setUp(self):
        self.login_url = reverse('login')
        self.user_data = {'username': 'bot', 'password': 'botbot'}
        return super().setUp()

    @classmethod
    def login(self, client, login_url, user_data):
        user = User.objects.get(username=user_data['username'])
        user.set_password(user_data['password'])
        user.save()
        response = client.post(login_url, user_data, format="json")
        return response.data['tokens']['access']

    @classmethod
    def get_authenticated_client(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return client

    def tearDown(self):
        return super().tearDown()
