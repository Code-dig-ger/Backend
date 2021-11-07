from .test_setup import TestSetUp
from django.urls import reverse


class TestUpsolve(TestSetUp):
    def test_problem_filter(self):
        # Deprecated
        test_url = reverse('problems')
        res = self.client.get(test_url,
                              data={"difficulty": "B"},
                              format="json")
        print(res.json())
