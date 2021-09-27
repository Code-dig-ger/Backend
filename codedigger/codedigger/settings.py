"""
Django settings for codedigger project.
Generated by 'django-admin startproject' using Django 3.1.4.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime

# for env file
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = [
    'localhost', 'api.codedigger.tech', '127.0.0.1', '128.199.26.91',
    '165.232.186.106'
]

AUTH_USER_MODEL = 'user.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Local
    'social_auth',
    'user',
    'codeforces',
    'problem',
    'lists',
    'blog',
    'contest',

    #Third Party
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_crontab',
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #extra
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'codedigger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'codedigger.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = [
#     "http://127.0.0.1:8000",
# ]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY':
    'error',
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('rest_framework_simplejwt.authentication.JWTAuthentication', )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=60),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=365),
}

CRONJOBS = [
    ('0 15 1 * *',
     'problem.cron.update_spoj'),  # Every month at day 1 at 3:00 PM
    ('0 13 * * 2', 'codeforces.cron.codeforces_update_users'
     ),  # Every week on Tuesday at 1:00PM
    ('0 22 * * *', 'problem.cron.update_codechef'),  # Everyday 22:00
    ('0 21 * * *', 'problem.cron.update_atcoder'),  # Everyday 21:00
    ('0 20 * * *', 'problem.cron.update_uva'),  # Everyday 20:00
    ('0 10 * * 2', 'codeforces.cron.codeforces_update_contest'
     ),  # Every week on Tuesday at 10:00
    ('0 0 * * *',
     'codeforces.cron.codeforces_update_problems'),  # Every day at 00:00 
    #('30 1 * * *'    , 'lists.cron.updater'), # Every day at 1:30 AM,
    ('0 1 * * *', 'lists.cron.codeforces_updater'),
    ('0 5 * * *', 'lists.cron.uva_updater'),
    ('0 9 * * *', 'lists.cron.codechef_updater'),
    ('0 13 * * *', 'lists.cron.atcoder_updater'),
    ('0 17 * * *', 'lists.cron.spoj_updater'),
    ('*/10 * * * *',
     'codeforces.cron.ratingChangeReminder'),  # Every 10th minute 

    # Short Code Contest
    #('*/15 * * * *' , 'contest.cron.update_codeforces_short_code_contests'), # Every 15th minute
]
CRONTAB_LOCK_JOBS = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
