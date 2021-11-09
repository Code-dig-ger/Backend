from .scrapers import update_atcoder_problems

from django.shortcuts import render
from codedigger.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def update_atcoder():
    subject = 'Atcoder Problem Update Process Started'
    message = 'Hope you are enjoying our Problems'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
              message,
              EMAIL_HOST_USER, [recepient],
              fail_silently=False)
    update_atcoder_problems()
    subject = 'Atcoder Problem Update Process Finished'
    message = 'Hope you are enjoying our Problems'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
              message,
              EMAIL_HOST_USER, [recepient],
              fail_silently=False)