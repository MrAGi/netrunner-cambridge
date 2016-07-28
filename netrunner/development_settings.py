# -*- coding: utf-8 -*-

from .settings import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['LOCAL_DB_NAME'],
        'USER': os.environ['LOCAL_DB_USER'],
        'PASSWORD': os.environ['LOCAL_DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}