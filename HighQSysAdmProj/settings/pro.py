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

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'same-origin'
