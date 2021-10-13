from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self):
        # set up test case do some calculation
        return super().setUp()

    def tearDown(self):
        # test case end , revert back changes to be made after test case end
        return super().tearDown()
