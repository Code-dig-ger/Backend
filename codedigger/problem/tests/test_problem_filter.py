from .test_setup import TestSetUp
from django.urls import reverse


class TestUpsolve(TestSetUp):
    def test_simple(self):
        test_url = reverse('problems')
        res = self.client.get(test_url,
                              format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data['result']), 20)

    def test_rating(self):
        test_url = reverse('problems')
        res = self.client.get(test_url,
                              data={
                                  'range_r': 1500
                              },
                              format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        for prob in data['result'] : 
            self.assertTrue(
                prob['platform']=='Atcoder' or \
                (prob['platform']=='Codechef' and prob['difficulty']!=None) or \
                prob['rating']%100 == 0
            )
        

