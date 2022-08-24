from celery import shared_task
from PostBlog.settings import EMAIL_HOST_USER
from user.models import User
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

logger = get_task_logger(__name__)

@shared_task()
def send_email_task():

    user = User.objects.all().last()
    mail_subject = " Registration Conformation"
    message = "Congratulations ! You are successfully registered. "
    to_email = user.email

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True
    )

    return "done"
