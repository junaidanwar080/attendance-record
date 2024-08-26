
from celery import shared_task
from time import sleep
from django.core.mail import send_mail

@shared_task
def sleepy(duration):
    sleep(duration)
    return None
@shared_task
def send_mail_task():
    send_mail(
        subject='CELERY_WORKED_YEAH',
        message="CELERY IS COOL",
        from_email='shaistatabbasum24@gmail.com',
        recipient_list=['shaistatabbasum523@gmail.com'],
        fail_silently=False,
    )
    return None
