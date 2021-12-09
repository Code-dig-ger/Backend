from rest_framework.test import APITestCase
from django.urls import reverse
#from faker import Faker

from user.models import User, Profile
from lists.models import List, Solved, ListInfo
from problem.models import Problem

from lists.test_fixtures.profile_fixtures import profile1, profile2


class TestSetUp(APITestCase):
    fixtures = [
        "user.json", "problems.json", "lists.json", "list_info.json",
        "solved.json"
    ]

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        Profile.objects.filter(owner=1).update(**profile1)
        Profile.objects.filter(owner=2).update(**profile2)

    @classmethod
    def login(self, client, login_url, user_data):
        user = User.objects.get(username=user_data['username'])
        user.set_password(user_data['password'])
        user.save()
        response = client.post(login_url, user_data, format="json")
        return response.data['tokens']['access']

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        #self.fake = Faker()

        self.user_data = {
            # 'email': 'testing@gmail.com',#self.fake.email(),
            'username': 'testing',  #self.fake.email().split('@')[0],
            'password': 'QWERTY@123'  #self.fake.email(),
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
