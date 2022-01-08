from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from user.models import Profile, User
from lists.test_fixtures.profile_fixtures import profile1, profile2

class TestSetUp(APITestCase):

    # def setUp(self):
    #     # set up test case do some calculation
    #     return super().setUp()

    fixtures = [
        "user.json", "cc_problems.json", "cc_contests.json", "cc_contest_problem.json"
        ]

    @classmethod
    def setUpTestData(cls):
        Profile.objects.filter(owner=1).update(**profile1)
        Profile.objects.filter(owner=2).update(**profile2)

    def setUp(self):
        self.login_url = reverse('login')
        self.user_data = {'username': 'testing', 'password': 'QWERTY@123'}
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
