from rest_framework.test import APITestCase
from django.urls import reverse
#from faker import Faker

from user.models import User


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        #self.fake = Faker()

        self.user_data = {
            'email': 'shivam@mail.com',#self.fake.email(),
            'username': 'shivam',#self.fake.email().split('@')[0],
            'password': 'QWERTY@123'#self.fake.email(),
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
