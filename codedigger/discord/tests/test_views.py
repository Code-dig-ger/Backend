from .test_setup import TestSetUp
from django.urls import reverse
from user.models import User, Profile

class TestUpsolve(TestSetUp):
    def test_verify(self):
        test_url = reverse('verify-discord')
        token = self.login(self.client, self.login_url, self.user_data)
        client = self.get_authenticated_client(token)

        data = {
            'username': 'testing',
            'discord_tag': 'aaradhya#2020'
        }
        response = client.put(test_url, data, format="json")
        profile = Profile.objects.get(owner = 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.is_discord_verified, True)
