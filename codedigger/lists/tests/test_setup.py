from rest_framework.test import APITestCase
from django.urls import reverse
#from faker import Faker

from user.models import User, Profile
from lists.models import List, Solved, ListInfo
from problem.models import Problem


class TestSetUp(APITestCase):
    fixtures = [
        "user.json", "problems.json", "lists.json", "profiles.json",
        "list_info.json"
    ]

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
        #delete all data in models if you want to use --keepdb
        Solved.objects.all().delete()
        ListInfo.objects.all().delete()
        List.objects.all().delete()
        Problem.objects.all().delete()
        User.objects.all().delete()
        Profile.objects.all().delete()
        return super().tearDown()
