from celery import shared_task
from django.core.mail import send_mail
from django.core.management import call_command

from PostBlog.settings import EMAIL_HOST_USER
from blog.models import Comment
from user.models import User
# from celery.decorators import periodic_task
from celery.schedules import crontab


@shared_task(run_every=crontab())
def comment_mail():
    user = User.objects.all().last()
    comment = Comment.objects.all().last()
    mail_subject = " Thank you ! "
    message = "Hello {} Thank you for visiting our site" \
              " and your comment for blog - {} and your comment is -{} ".format(user.username, comment.blog.title,
                                                                                comment.body)
    print(user.email)
    to_email = user.email

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True
    )
    return "done"


@shared_task()
def execute_file():
    print(
        "Here I am helping you."
    )
    call_command("last_five_hour_file",)
