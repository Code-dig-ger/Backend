from user.models import Profile, User
from user.exception import ValidationException


def get_user(username):
    try:
        user = User.objects.get(username=username)
        if user.is_verified:
            return user
        else:
            raise ValidationException(
                'You haven\'t verified your email. Please login again to get a verification email'
            )
    except:
        raise ValidationException(
            'User doesn\'t exists. Please check your username or register yourself on https://codedigger.tech'
        )


def get_user_profile(user):
    profile = Profile.objects.get(owner=user)
    if profile.codeforces == None or profile.codeforces == "":
        raise ValidationException(
            'User haven\'t activated his Profile. Please login to https://codedigger.tech to activate.'
        )
    else:
        return profile
