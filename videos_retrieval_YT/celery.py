import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videos_retrieval_YT.settings")
app = Celery("videos_retrieval_YT")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    "fetch-videos-every-10-min": {
        'task': 'api.tasks.store_video_data',
        'schedule': 10.0
    }
}
