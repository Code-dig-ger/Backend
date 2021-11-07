from .test_setup import TestSetUp
from django.urls import reverse


class TestUpsolve(TestSetUp):
    test_url = reverse('problems')

    def test_simple(self):
        res = self.client.get(self.test_url, format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data['result']), 20)

    def test_rating(self):
        res = self.client.get(self.test_url,
                              data={'range_r': 1500},
                              format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        for prob in data['result']:
            self.assertTrue(
                prob['platform']=='Atcoder' or \
                (prob['platform']=='Codechef' and prob['difficulty']!=None) or \
                prob['rating']%100 == 0
            )

    def test_platform(self):
        res = self.client.get(self.test_url,
                              data={'platform': 'C,A'},
                              format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        for prob in data['result']:
            self.assertTrue(prob['platform'] == 'Atcoder'
                            or prob['platform'] == 'Codechef')

    def test_index(self):
        res = self.client.get(self.test_url,
                              data={'index': 'a,b'},
                              format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        for prob in data['result']:
            self.assertTrue(prob['index'].lower() == 'a'
                            or prob['index'].lower() == 'b')

    def test_tags(self):
        res = self.client.get(self.test_url,
                              data={
                                  'and_in_tags': True,
                                  'tags': 'greedy,graph'
                              },
                              format="json")
        for prob in res.json()['result']:
            self.assertTrue('greedy' in prob['tags']
                            and 'graph' in prob['tags'])

    def test_mentor_solved(self):
        token = self.login(self.client, self.login_url, self.user_data)
        client = self.get_authenticated_client(token)
        res = client.get(self.test_url, data={'mentor': True}, format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data['result']), 3)

    def test_hide_solved(self):
        token = self.login(self.client, self.login_url, self.user_data)
        client = self.get_authenticated_client(token)
        res = client.get(self.test_url,
                         data={
                             'mentor': True,
                             'hide_solved': True
                         },
                         format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data['result']), 1)
    
    def test_solved_by(self):
        res = self.client.get(self.test_url,
                              data={
                                  'solved_by': 'testing'
                              },
                              format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data['result']), 2)
