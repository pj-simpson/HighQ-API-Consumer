from django.db import models
from django.utils import timezone


class OauthToken(models.Model):
    access_token = models.CharField(max_length=128)
    access_token_expires = models.DateTimeField(blank=False, default=timezone.now)
    refresh_token = models.CharField(max_length=128)
    refresh_token_expires = models.DateTimeField(blank=True, default=timezone.now)
    gen_time = models.DateTimeField(blank=False, default=timezone.now)
