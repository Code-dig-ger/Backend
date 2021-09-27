def rating_to_rank(rating):
    if rating < 1200:
        return "newbie"
    elif rating < 1400:
        return "pupil"
    elif rating < 1600:
        return "specialist"
    elif rating < 1900:
        return "expert"
    elif rating < 2100:
        return "candidate master"
    elif rating < 2300:
        return "master"
    elif rating < 2400:
        return "international master"
    elif rating < 2600:
        return "grandmaster"
    elif rating < 3000:
        return "international grandmaster"
    else:
        return "legendary grandmaster"


def rating_to_color(rating):
    if rating < 1200:
        return "user-gray"
    elif rating < 1400:
        return "user-green"
    elif rating < 1600:
        return "user-cyan"
    elif rating < 1900:
        return "user-blue"
    elif rating < 2100:
        return "user-violet"
    elif rating < 2400:
        return "user-orange"
    else:
        return "user-red"


def islegendary(rating):
    if rating >= 3000:
        return True
    else:
        return False
