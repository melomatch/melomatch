import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "melomatch.settings")

app = Celery("soil")
app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()
