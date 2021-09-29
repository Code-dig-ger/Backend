from django.template import Context, Template
from django.utils.html import strip_tags
from django.core.mail import send_mail
from codedigger.settings import EMAIL_HOST_USER

from user.models import Profile
from .models import user, user_contest_rank
from .email.rating_reminder import get_rating_reminder_string
from .serializers import contestRankSerializer

def rating_to_difficulty(rating):
    if rating <= 1100:
        return 'B'
    elif rating <= 1500:
        return 'E'
    elif rating <= 1800:
        return 'M'
    elif rating <= 2100:
        return 'H'
    elif rating <= 2600:
        return 'S'
    else:
        return 'C'

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


def send_testing_mail(sub):
    subject = sub
    message = 'This is a testing mail send to our testing account.'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)

def send_error_mail(sub):
    subject = sub
    message = 'OOPS: An error found. This is an error mail send to know error.'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)

def sendMailToUsers(rating_changes, new_contest):
    users = Profile.objects.all()
    send_testing_mail(
        'Sending Mail for Rating Change ' + rating_changes[0]['contestName']
    )

    for rating_change in rating_changes:
        user_profile = users.filter(codeforces__iexact=rating_change['handle'])
        if user_profile.exists():
            codeforces_user = user.objects.filter(
                handle=rating_change['handle']
            )
            cdata = None
            if codeforces_user.exists():
                ucr = user_contest_rank.objects.filter(user=codeforces_user[0],
                                                       contest=new_contest)
                if ucr.exists():
                    cdata = contestRankSerializer(ucr[0]).data
            
            rating_change.update({
                'oldRank': rating_to_rank(rating_change['oldRating']),
                'newRank': rating_to_rank(rating_change['newRating']),
                'oldcolor': rating_to_color(rating_change['oldRating']),
                'newcolor': rating_to_color(rating_change['newRating']),
                'isoldlegendary': islegendary(rating_change['oldRating']),
                'isnewlegendary': islegendary(rating_change['newRating'])
            })

            subject = 'Codeforces Rating Updated'
            recepient = [user_profile[0].owner.email]

            template = Template(get_rating_reminder_string())
            context = Context({'rating_change': rating_change, 'cdata': cdata})
            html_message = template.render(context)
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, EMAIL_HOST_USER, recepient,
                      html_message=html_message, fail_silently=True)