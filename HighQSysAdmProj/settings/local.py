from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

THUMBNAIL_DEBUG = True

# local env variable for shell
# export
#DJANGO_SETTINGS_MODULE=HighQSysAdmProj.settings.local


