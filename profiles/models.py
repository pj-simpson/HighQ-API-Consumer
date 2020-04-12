from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True,null=True,max_length=20)
    contact_email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)