from django.db import models
from api.constants import YT_BASE_URL


class Video(models.Model):
    youtube_video_id = models.CharField(max_length=11, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000, blank=True, null=True)
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Title:{str(self.title)}\nURL:{YT_BASE_URL + str(self.youtube_video_id)}'


class APIKey(models.Model):
    api_key = models.CharField(max_length=50, unique=True)
    has_expired = models.BooleanField(default=False, null=False)