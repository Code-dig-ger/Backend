import requests

from user.exception import ValidationException

BASEURL = "https://uhunt.onlinejudge.org/api/"

def validated_response(response):
    # Check for exceptions and raise if any
    # If no exception, send response dict

    if response.status_code >= 500:
        raise ValidationException('Uhunt API: Server Error')
    elif response.status_code != 200:
        raise ValidationException('Uhunt API: Bad Request')

    response_dict = response.json()
    return response_dict

def username_to_id(username):
    """
        return userId (integer) of username if username is valid 
        else 0 (status_code 200 in both case)
    """
    url = BASEURL + "uname2uid/{}".format(username)
    response = requests.get(url)
    return validated_response(response)

def problem_list():
    """
    return list of 
        0. Problem ID
        1. Problem Number
        2. Problem Title
        3. Number of Distinct Accepted User (DACU)
        4. Best Runtime of an Accepted Submission
        5. Best Memory used of an Accepted Submission
        6. Number of No Verdict Given (can be ignored)
        7. Number of Submission Error
        8. Number of Can't be Judged
        9. Number of In Queue
        10. Number of Compilation Error
        11. Number of Restricted Function
        12. Number of Runtime Error
        13. Number of Output Limit Exceeded
        14. Number of Time Limit Exceeded
        15. Number of Memory Limit Exceeded
        16. Number of Wrong Answer
        17. Number of Presentation Error
        18. Number of Accepted
        19. Problem Run-Time Limit (milliseconds)
        20. Problem Status 
        (0 = unavailable, 1 = normal, 2 = special judge)
    """
    url = BASEURL + "p"
    response = requests.get(url)
    return validated_response(response)

def user_submission(user_id):
    """
    return
        name : the name of the user
        uname : the username of the user
        subs : the submissions of the user (as an array)

        The subs array length is the same as 
        the number of submissions of the user. 
        Each element is one submission with values:

        0. Submission ID
        1. Problem ID
        2. Verdict ID
        3. Runtime
        4. Submission Time (unix timestamp)
        5. Language ID 
        (1=ANSI C, 2=Java, 3=C++, 4=Pascal, 5=C++11)
        6. Submission Rank
        7. Verdict ID can be one of the following values:

        10 : Submission error
        15 : Can't be judged
        20 : In queue
        30 : Compile error
        35 : Restricted function
        40 : Runtime error
        45 : Output limit
        50 : Time limit
        60 : Memory limit
        70 : Wrong answer
        80 : PresentationE
        90 : Accepted
    """

    url = BASEURL + "subs-user/{}".format(user_id)
    response = requests.get(url)
    return validated_response(response)

def cpbook(version = 3):
    """
    The exercises is an array of chapter. 
    Each chapter has a title and arr attribute which contains the sub-chapters. 
    Each sub-chapter also has a title and arr attribute which contains the sub-sub-chapters. 
    Each sub-sub-chapter is formatted as an array where 
        the first element is the title of the sub-sub-chapter and 
        the second element onwards are the problem numbers associated with it. 
    The negative problem number signify that it is a starred problem
    """
    url = BASEURL + "cpbook/{}".format(version)
    response = requests.get(url)
    return validated_response(response)