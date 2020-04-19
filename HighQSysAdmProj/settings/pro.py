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

THUMBNAIL_DEBUG = False


# local env variable for shell
# export DJANGO_SETTINGS_MODULE=HighQSysAdmProj.settings.pro