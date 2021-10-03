from user.exception import ValidationException

from .api import (contest_list, contest_ratingChanges, contest_standings,
                  user_ratedList)
from .models_utils import (create_or_update_contest, create_or_update_problem,
                           create_or_update_user, update_and_save_contest_data)
from .models import contest, user_contest_rank
from .utils import send_error_mail, sendMailToUsers


def ratingChangeReminder():

    try:
        contests = contest_list()
    except:
        return

    limit = 1

    for codeforces_contest in contests:

        try:
            response = contest_ratingChanges(codeforces_contest['id'])
            new_contest = create_or_update_contest(codeforces_contest)

            if len(response) == 0:
                continue
            elif not new_contest.isUpdated:
                new_contest.isUpdated = True
                new_contest.save()
                update_and_save_contest_data(response, new_contest)
                sendMailToUsers(response, new_contest)
            elif limit:
                limit -= 1
            else:
                break

        except:
            check_contest = contest.objects.filter(contestId=id)
            if not check_contest.exists():
                continue
            elif check_contest[0].isUpdated:
                break
            else:
                continue


def codeforces_update_users():

    try:
        response = user_ratedList(activeOnly=True)
    except ValidationException as err:
        send_error_mail(str(err))
        return

    for codeforces_user in response:
        create_or_update_user(codeforces_user)


def codeforces_update_problems():

    try:
        contests = contest_list()
    except ValidationException as err:
        return

    for codeforces_contest in contests[:50]:

        try:
            response = contest_standings(contestId=codeforces_contest['id'],
                                         count=1)
        except ValidationException as err:
            continue

        create_or_update_contest(codeforces_contest)
        for contest_problem in response['problems']:
            create_or_update_problem(contest_problem)

    try:
        contests = contest_list(gym=True)
    except ValidationException as err:
        return

    for codeforces_contest in contests[-50:]:
        try:
            response = contest_standings(contestId=codeforces_contest['id'],
                                         count=1)
        except ValidationException as err:
            continue

        create_or_update_contest(codeforces_contest, contest_type='G')
        for contest_problem in response['problems']:
            create_or_update_problem(contest_problem, type="gym")


def codeforces_update_contest():

    try:
        response = contest_list()
    except ValidationException as err:
        send_error_mail(str(err))
        return

    response.reverse()

    for codeforces_contest in response[-50:]:

        try:
            contest_rating_change = contest_ratingChanges(
                codeforces_contest['id'])
        except:
            continue

        new_contest = create_or_update_contest(codeforces_contest)

        if user_contest_rank.objects.filter(contest=new_contest).count() == \
                            len(contest_rating_change):
            continue
        update_and_save_contest_data(contest_rating_change, new_contest)
