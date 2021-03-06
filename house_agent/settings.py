"""
Django settings for house_agent project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import django_redis

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sh7g(i420xgfpk@4q=0w#y7y4wgzci7z*h@ii0p72*5&mb*amc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django_filters',
    'rest_framework',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'house_helper.apps.HouseHelperConfig',
    'multi_captcha_admin',
    'django.contrib.admin',
    'captcha',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'house_agent.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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
# ??????????????????
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     '*'
# )
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
WSGI_APPLICATION = 'house_agent.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # ???????????????
        'NAME': 'house_helper',  # ??????????????????????????????
        'USER': 'root',  # ????????????????????????????????????
        'PASSWORD': '123456',  # ??????
        'HOST': '192.168.136.128',  # mysql?????????????????????ip
        'PORT': '3306',  # mysql????????????
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# ???????????????
MULTI_CAPTCHA_ADMIN = {
    'engine': 'simple-captcha',  # ??????recaptcha2
}
# ?????????????????????
CAPTCHA_IMAGE_SIZE = (78, 35)
# ????????????
CAPTCHA_LENGTH = 4
# ??????
CAPTCHA_TIMEOUT = 1

# ??????redis??????
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',  # ???????????? Redis
        # ??????Redis?????????(???????????????)
        # ???????????????(???????????????Redis??????????????????????????????????????????)
        'LOCATION': [
            'redis://192.168.136.128:6379/0',
        ],
        'KEY_PREFIX': 'house_helper',  # ???????????????????????????
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',  # ????????????(???????????????)
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 512,  # ??????????????????(????????????)
            },
            # 'PASSWORD': '123456',
        }
    }
}

# session???????????????
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# ??????session????????????,????????????
SESSION_COOKIE_AGE = 60 * 60 * 8

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # ?????????json??????
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    # ??????????????????
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    # # ????????????
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'house_agent.Authentication.LoginAuth',
    # ],
    # ?????????????????????
    'DEFAULT_PAGINATION_CLASS': 'house_helper.MyPagination.MyPageNumberPagination',
    # ????????????
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

AUTH_USER_MODEL = 'house_helper.User'

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
