from codedigger.settings import EMAIL_HOST_USER
from django.core.mail import send_mail	

class Util:
    @staticmethod
    def send_email(data):
        send_mail(data['email_subject'],data['email_body'],EMAIL_HOST_USER,[data['to_email']])