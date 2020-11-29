from django.db import models


class OauthToken(models.Model):
    access_token = models.CharField(max_length=128)
    access_token_expires = models.DateTimeField(null=True)
    refresh_token = models.CharField(max_length=128)
    refresh_token_expires = models.DateTimeField(null=True)
    gen_time = models.DateTimeField(auto_now_add=True)
