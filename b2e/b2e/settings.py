"""
Django settings for b2e project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '69rp&7cet6#3m&(%if5)4$#98!4_f8unw(o71il#sr&5lu9!5c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# 請增加允許的 FQDN
ALLOWED_HOSTS = ['b2e.com']


# Application definition

INSTALLED_APPS = [
    'home',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'b2e.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates/',
            BASE_DIR + '/home/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'b2e.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'b2e',
        'USER':'b2e_user',
        'PASSWORD':'0ioaN3QpZr8ugXtk',
        'HOST':'mysql57',
        'PORT':'3306'
    }
}
# mysql57

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
# 中文
LANGUAGE_CODE = 'zh-Hant'
# 時區
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
ADMIN_MEDIA_PREFIX = '/static/admin'

import sys
import io
if sys.version_info[0] == 3:
    # fix UTF8 problem (目前經驗是 py 3.6 以下， 3.7 以上沒這問題)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Log 設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'b2e_custom': {
            'format' : "%(asctime)s - [%(levelname)s][%(name)s.%(module)s.%(funcName)s:%(lineno)s] %(message)s",
            'datefmt' : "%Y-%b-%d %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/b2e.log',
            'formatter': 'b2e_custom',
            'encoding':'utf-8'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'home.views': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'home.models': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'home.forms': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
