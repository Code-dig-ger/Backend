from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    fixtures = [
        "cf_users.json"
    ]

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
