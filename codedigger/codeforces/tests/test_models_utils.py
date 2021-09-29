from .test_setup import TestSetUp
from codeforces.test_fixtures.models_utils_fixture import (cf_user, cf_contest,
                                                           cf_problem,
                                                           rating_change_data)
from codeforces.models_utils import (create_or_update_user,
                                     create_or_update_contest,
                                     create_or_update_problem,
                                     update_and_save_contest_data)

from codeforces.models import user, contest, user_contest_rank
from problem.models import Problem


class TestViews(TestSetUp):
    def test_create_user(self):
        newUser = create_or_update_user(cf_user)
        users = user.objects.filter(handle=cf_user['handle'])
        self.assertEqual(users.exists(), True)
        self.assertEqual(newUser.rating, cf_user['rating'])
        self.assertEqual(users[0].organization.name, cf_user['organization'])

    def test_create_contest(self):
        newContest = create_or_update_contest(cf_contest)
        contests = contest.objects.filter(contestId=cf_contest['id'])
        self.assertEqual(contests.exists(), True)
        self.assertEqual(newContest.name, cf_contest['name'])
        self.assertEqual(contests[0].startTime, cf_contest['startTimeSeconds'])

    def test_create_problem(self):
        newProblem = create_or_update_problem(cf_problem)
        problems = Problem.objects.filter(
            prob_id=str(cf_problem['contestId']) + cf_problem['index'])
        self.assertEqual(problems.exists(), True)
        self.assertEqual(newProblem.rating, cf_problem['rating'])
        self.assertEqual(problems[0].contest_id, str(cf_problem['contestId']))

    def test_update_contest_rank(self):
        newContest = create_or_update_contest(cf_contest)
        create_or_update_user(cf_user)
        update_and_save_contest_data(rating_change_data, newContest)

        qs = user_contest_rank.objects.filter(contest = newContest)\
                                        .order_by('worldRank')
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0].worldRank, 1)
        self.assertEqual(qs[0].user.handle, rating_change_data[0]['handle'])
        self.assertEqual(qs[1].user.handle, rating_change_data[1]['handle'])
