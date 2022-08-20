from django.db import models


class APIKey(models.Model):
    api_key = models.CharField(max_length=50, unique=True)
    has_expired = models.BooleanField(default=False, null=False)