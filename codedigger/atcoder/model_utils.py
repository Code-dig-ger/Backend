from problem.models import Problem, atcoder_contest


def create_or_update_contest(contest):
    new_contest = atcoder_contest.objects.get_or_create(
        contestId=contest['id'],
        defaults={
            'name': contest['title'],
            'startTime': contest['start_epoch_second'],
            'duration': contest['duration_second']
        })
    cur = atcoder_contest.objects.get(contestId=contest['id'])
    print(cur)


def create_or_update_problem(problem):
    new_problem = Problem.objects.get_or_create(
        prob_id=problem['id'],
        platform='A',
        defaults={
            'name':
            problem['title'],
            'contest_id':
            problem['contest_id'],
            'url':
            "https://atcoder.jp/contests/{}/tasks/{}".format(
                problem['contest_id'], problem['id']),
            'index':
            problem['id'].split("_")[-1]
        })
