from .base import *

DEBUG = False

ALLOWED_HOSTS = ['www.highqsysadmin.com',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('PYTHONANYWHEREMYSQLDBNAME',default=''),
        'USER': config('PYTHONANYWHEREMYSQLDBUSER',default=''),
        'PASSWORD': config('PYTHONANYWHEREMYSQLDBPASS',default=''),
        'HOST': config('PYTHONANYWHEREMYSQLDBHOST',default=''),
    }
}

