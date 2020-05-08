from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.apps import apps

from phonenumber_field.modelfields import PhoneNumberField

import tasks as T

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_profile')
    phone_number = PhoneNumberField(blank=True, default='')
    contact_email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', default='no_image.png')

    def is_user_firstline(self):
        if self.user in User.objects.filter(groups=1):
            return True

    def is_user_secondline(self):
        if self.user in User.objects.filter(groups=2):
            return True

    def get_posted(self):
        return T.models.Task.objects.all().filter(poster_id=self.user_id)

    def get_assigned(self):
        return T.models.Task.objects.all().filter(asignee_id=self.user_id)

