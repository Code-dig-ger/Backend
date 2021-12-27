# Python Libraries
import requests

# User App
from user.exception import ValidationException


def validated_response(response):
    # Check for exceptions and raise if any
    # If no exception, send response dict

    if response.status_code >= 500:
        raise ValidationException('Codeforces API: Server Error')
    elif response.status_code != 200:
        raise ValidationException('Codeforces API: Bad Request')

    response_dict = response.json()
    if response_dict['status'] != 'OK':
        raise ValidationException(response_dict['comment'])

    return response_dict['result']


def user_info(handles: list):
    # param :
    # handles : a list of handles to get information
    # return :
    # list of codeforces information of handles provided

    url = "https://codeforces.com/api/user.info"
    payload = {'handles': ';'.join(handles)}
    response = requests.get(url=url, params=payload)
    return validated_response(response)


def user_rating(handle):
    # param : Codeforces user handle
    # handle : Codeforces user handle.
    # return : Returns rating history of the specified user

    url = "https://codeforces.com/api/user.rating"
    payload = {'handle': handle}
    response = requests.get(url=url, params=payload)
    return validated_response(response)


def user_ratedList(activeOnly=False):
    # params :
    # If true then only users, who participated in rated contest
    # during the last month are returned.
    # return :
    # Returns the list users who have participated in at least
    # one rated contest.

    url = "https://codeforces.com/api/user.ratedList"
    payload = {'activeOnly': activeOnly}

    response = requests.get(url=url, params=payload)
    return validated_response(response)


def contest_list(gym=False):
    # params :
    # If true — than gym contests are returned.
    # Otherwide, regular contests are returned.
    # return :
    # List of Gym/ Regular Contest

    url = "https://codeforces.com/api/contest.list"
    payload = {'gym': gym}
    response = requests.get(url=url, params=payload)
    return validated_response(response)


def contest_standings(contestId,
                      standing_from=1,
                      count=None,
                      handles=None,
                      room=None,
                      showUnofficial=False):
    # param :
    # contestId: Id of the contest
    # from: 1-based index of the standings row to start the ranklist.
    # count: Number of standing rows to return
    # handles: list of handles
    # room : If specified, than only participants from this room will be shown
    # showUnofficial: If true than all participants (virtual, out of competition) are shown

    # return
    # the description of the contest and the requested part of the standings.
    # Returns object with three fields: "contest", "problems" and "rows".
    # Field "contest" contains a Contest object.
    # Field "problems" contains a list of Problem objects.
    # Field "rows" contains a list of RanklistRow objects.

    url = "https://codeforces.com/api/contest.standings"
    payload = {
        'contestId': contestId,
        'from': standing_from,
        'showUnofficial': showUnofficial
    }
    if count:
        payload['count'] = count
    if handles:
        payload['handles'] = ';'.join(handles)
    if room:
        payload['room'] = room

    response = requests.get(url=url, params=payload)
    return validated_response(response)


def contest_ratingChanges(contestId):
    # param :
    # contestId : id of contest
    # Returns rating changes after the contest.

    url = "https://codeforces.com/api/contest.ratingChanges"
    payload = {'contestId': contestId}
    response = requests.get(url=url, params=payload)
    return validated_response(response)


def user_status(handle, starting_from=1, count=None):
    # param :
    # handle : Codeforces user handle.
    # from : 1-based index of the first submission to return.
    # count: Number of returned submissions.
    # returns :
    # list of results if exists else raise exception
    HANDLES = (
        'vjudge1 vjudge2 vjudge3 vjudge4 vjudge5 '
        'luogu_bot1 luogu_bot2 luogu_bot3 luogu_bot4 luogu_bot5').split()

    if handle in HANDLES:
        raise ValidationException('This Handle can\'t be processed')

    payload = {'handle': handle, 'from': starting_from}
    if count != None:
        payload['count'] = count
    url = "https://codeforces.com/api/user.status"
    response = requests.get(url, params=payload)
    return validated_response(response)

def contest_submissions(contestId,handle=None,from_=1,count=1000):
    url = "https://codeforces.com/api/contest.status"
    payload = {
        'contestId': contestId,
        'handle': handle,
        'from': from_,
        'count': count
    }

    response = requests.get(url=url, params=payload)
    return validated_response(response)