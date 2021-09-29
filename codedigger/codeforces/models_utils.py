# Local App Import
from .api import user_info
from .models import organization, country, user, contest, user_contest_rank
from .utils import send_error_mail, rating_to_difficulty

# Problem App Import 
from problem.models import Problem

# User App Import
from user.exception import ValidationException

def create_or_update_user(codeforces_user):
    # param: 
        # codeforces_user: Response from Codeforces
    # This function will update our Codeforces User Object 
    # and Sava to Database

    newUser, created =  user.objects.get_or_create(
                            handle=codeforces_user['handle']
                        )

    name = ""
    if 'firstName' in codeforces_user:
        name += codeforces_user['firstName']
        name += " "
    if 'lastName' in codeforces_user:
        name += codeforces_user['lastName']

    if len(name) > 100:
        name = name[:100]

    newUser.name = name
    if 'rating' in codeforces_user:
        newUser.rating = codeforces_user['rating']
        newUser.maxRating = codeforces_user['maxRating']
        newUser.rank = codeforces_user['rank']
        newUser.maxRank = codeforces_user['maxRank']

    newUser.photoUrl = codeforces_user['titlePhoto'][2:]

    if 'country' in codeforces_user:
        obj, created = country.objects.get_or_create(
            name=codeforces_user['country'])
        newUser.country = obj

    if 'organization' in codeforces_user:
        obj, created = organization.objects.get_or_create(
            name=codeforces_user['organization'])
        newUser.organization = obj

    newUser.save()
    return newUser


def create_or_update_contest(codeforces_contest, contest_type = 'R'):
    # param :
        # codeforces_contest : response of codeforces contest
        # contest_type: Regular 'R' or Gym 'G'
    
    # This function will update and save contest model
    new_contest, created =   contest.objects.get_or_create(
                        contestId = codeforces_contest['id']
                    )

    if 'startTimeSeconds' in codeforces_contest:
        new_contest.startTime = codeforces_contest['startTimeSeconds']

    new_contest.Type = contest_type
    new_contest.contestId = codeforces_contest['id']
    new_contest.name = codeforces_contest['name']
    new_contest.duration = codeforces_contest['durationSeconds']
    new_contest.save()
    return new_contest


def create_or_update_problem(contest_problem, type = "contest"):
    # param : 
        # contest_problem : codeforces problem object 
        # type : contest problem or gym
    
    # This function will create or update problem 

    prob_id = str(contest_problem['contestId']) + contest_problem['index']
    new_problem, created =  Problem.objects.get_or_create(
                                prob_id=prob_id, platform='F'
                            )

    new_problem.name = contest_problem['name']
    new_problem.contest_id = contest_problem['contestId']
    
    new_problem.url = "https://codeforces.com/{}/{}/problem/{}".format(
        type, str(contest_problem['contestId']), contest_problem['index']
    )

    new_problem.index = contest_problem['index']
    new_problem.tags = contest_problem['tags']

    if 'rating' in contest_problem:

        new_problem.rating = contest_problem['rating']
        new_problem.difficulty = rating_to_difficulty(
                                    int(contest_problem['rating']))

    new_problem.save()
    return new_problem


def update_and_save_contest_data(data, new_contest):
    # param: 
        # data: Response of Codeforces User Rank Data
        # new_contest: Contest Model Object 
    # This function will update user contest rank

    for participant in data:
        user_handle = participant['handle']
        rank = participant['rank']
        
        contest_user, created = user.objects.get_or_create(handle=user_handle)

        ucr, ucr_created = user_contest_rank.objects.get_or_create(
            user=contest_user, contest=new_contest)

        if created:
            try: 
                codeforces_users = user_info([user_handle])
                create_or_update_user(codeforces_users[0])
            except ValidationException as err: 
                send_error_mail(str(err))
        else:
            contest_user.rating = participant['newRating']
            contest_user.maxRating = max(contest_user.maxRating,
                                        contest_user.rating)
            contest_user.save()

        ucr.worldRank = rank
        ucr.save()