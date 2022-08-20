import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videos_retrieval_YT.settings")
app = Celery("videos_retrieval_YT")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()