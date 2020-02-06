from datetime import datetime
from django.db import models

class OauthToken(models.Model):
    access_token = models.CharField(max_length=128)
    access_token_expires = models.DateTimeField(blank=False, default=datetime.now())
    refresh_token = models.CharField(max_length=128)
    refresh_token_expires = models.DateTimeField(blank=True,default=datetime.now())
    gen_time = models.DateTimeField(blank=False, default=datetime.now())


