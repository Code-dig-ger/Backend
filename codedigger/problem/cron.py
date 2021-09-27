from .scraper.spoj import scraper
from .scraper.uva import update_uva_problems
from .scraper.atcoder import update_atcoder_problems
from .scraper.codechef import codeChefScraper

from django.shortcuts import render
from codedigger.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def update_spoj():
    #checking if cronjobs has started , you will get a mail
    subject = 'SPOJ Scraping Started'
    message = 'Hope you are enjoying our Problems'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
              message,
              EMAIL_HOST_USER, [recepient],
              fail_silently=False)
    scraper()
    subject = 'SPOJ Scraping Finished'
    message = 'Hope you are enjoying our Problems'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
              message,
              EMAIL_HOST_USER, [recepient],
              fail_silently=False)


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


def update_uva():
    subject = 'UVa Problem Update Process Started'
    message = 'Hope you are enjoying our Problems'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
              message,
              EMAIL_HOST_USER, [recepient],
              fail_silently=False)
    update_uva_problems()
    subject = 'UVa Problem Update Process Finished'
    message = 'Hope you are enjoying our Problems'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
              message,
              EMAIL_HOST_USER, [recepient],
              fail_silently=False)


def update_codechef():
    subject = 'Codechef Update Process Started'
    message = 'Hope you are enjoying our Problems'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
              message,
              EMAIL_HOST_USER, [recepient],
              fail_silently=False)
    codeChefScraper()
    subject = 'Codechef Update Process Finished'
    message = 'Hope you are enjoying our Problems'
    recepient = 'testing.codedigger@gmail.com'
    send_mail(subject,
              message,
              EMAIL_HOST_USER, [recepient],
              fail_silently=False)
