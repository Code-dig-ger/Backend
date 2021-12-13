from django.core.mail import send_mail
from codedigger.settings import EMAIL_HOST_USER


def send_testing_mail(sub):
    subject = sub
    message = 'This is a testing mail send to our testing account.'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
            message,
            EMAIL_HOST_USER, [recepient],
            fail_silently=False)


def send_error_mail(sub):
    subject = sub
    message = 'OOPS: An error found. This is an error mail send to know error.'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
            message,
            EMAIL_HOST_USER, [recepient],
            fail_silently=False)