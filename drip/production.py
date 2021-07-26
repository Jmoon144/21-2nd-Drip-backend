from .base import *

DEBUG = False

SECRET_KEY = 'django-insecure-2zdh6vdhr%eo8fx9*u=nl(_3yxa4c0#0nyh&ye%n-$wc9534#e'
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drip2',
        'USER': 'root',
        'PASSWORD': 'go9511455',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

ALGORITHM = "HS256"

ACCESS_KEY = "AKIAZBG6YDXQE4I2BEU6"
SECRET_ACCESS_KEY = "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"
