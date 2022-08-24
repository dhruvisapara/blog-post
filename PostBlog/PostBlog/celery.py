import os
from celery.schedules import crontab
from celery import Celery, shared_task
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PostBlog.settings")
app = Celery("PostBlog")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

app.conf.beat_schedule = {

    "execute_file": {
        "task": "blog.blog_api.task.execute_file",
        "schedule": crontab(minute="*/1"),
    }
}
# app.conf.beat_schedule = {
#
#     'comment_mail': {
#         'task': 'comment_mail',
#         'schedule': crontab(),
#     }}
# CELERYBEAT_SCHEDULE={
#
#     'comment_mail': {
#         'task': 'blog.blog_api.task.comment_mail',
#         'schedule': crontab(),
#     }}


# app.conf.beat_schedule = {
#     "execute_file": {
#         "task": "execute_file",
#         "schedule": crontab(minute="*/1"),
#     }}
