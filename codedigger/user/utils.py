from codedigger.settings import EMAIL_HOST_USER
from django.core.mail import send_mail	
from .email.send_mail import get_send_mail_string

class Util:
    @staticmethod
    def send_email(data):

    	#template = Template(get_send_mail_string())
		#context = Context({
		#	'username': data['email_body']['username'] ,
		#	'message' : data['email_body']['message'] ,
		#	'link' : data['email_body']['link'] 
		#})
		#html_message = template.render(context)
		#plain_message = strip_tags(html_message)

		#send_mail(data['email_subject'], plain_message, EMAIL_HOST_USER, [data['to_email']] , html_message=html_message, fail_silently = True)
        
        send_mail(data['email_subject'],data['email_body'],EMAIL_HOST_USER,[data['to_email']])