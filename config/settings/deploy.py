from .base import *

DEBUG = False

ALLOWED_HOSTS = ['mywebsite.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'New_DB_Music_Final',
        'USER': 'admin_go',
        'PASSWORD': '201400117',
        'HOST': 'database-music.ceun7fmwg3b4.us-east-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'" # strict mode 설정 추가
        }
    }
}