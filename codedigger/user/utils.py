from codedigger.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Util:

    @staticmethod
    def send_email(data):
        context = {
            'username': data['email_body']['username'],
            'message': data['email_body']['message'],
            'link': data['email_body']['link']
        }
        html_message = render_to_string('user/send_mail.html', context)
        plain_message = strip_tags(html_message)
        send_mail(data['email_subject'],
                  plain_message,
                  EMAIL_HOST_USER, [data['to_email']],
                  html_message=html_message,
                  fail_silently=True)

    #send_mail(data['email_subject'],data['email_body'],EMAIL_HOST_USER,[data['to_email']])
