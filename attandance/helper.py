from django.core.mail import send_mail

# Create your views here.
def send_mail_without_celery():
    send_mail('CELERY_WORKED_YEAH', "CELERY IS COOL",
   'shaistatabbasum24@gmail.com'
   ['shaistatabbasum523@gmail.com'],
   fail_silently=False

    )
    return None