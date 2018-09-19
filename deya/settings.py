import os
import socket


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5-y0wgn3f%d$2oxl&v-+5y3n#&z4*e4eh)lml2k9(s(0rl5r__'

DJANGO_SETTINGS_MODULE='deya.settings'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1  # αλλιως χτυπάει το default authentication system

# Application definition

INSTALLED_APPS = [
    'damage.apps.DamageConfig',
    #'damage',
     #django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',



    #external apps
    'crispy_forms',
    'widget_tweaks',
    'django_cool_paginator',


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

ROOT_URLCONF = 'deya.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'deya.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'damage',
        'USER': 'root',
        'PASSWORD': '3880046',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

######################################################################################
#  AUTHORIZATION
#######################################################################################
LOGIN_REDIRECT_URL = '/deyausers'
LOGOUT_REDIRECT_URL = '/frontpage'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

CRISPY_TEMPLATE_PACK = 'bootstrap3'

STATIC_URL = '/static/'

#################################################################################
# GOOGLE
################################################################################
GOOGLE_API_KEY = "AIzaSyDmdCbjHSXuma43DN3X8ihHuyU-rI3KKZY"

#################################################################################
# PAGINATION
#################################################################################
COOL_PAGINATOR_NEXT_NAME = "Eπόμενη"            #COOL_PAGINATOR options
COOL_PAGINATOR_PREVIOUS_NAME = "Προηγούμενη"

####################################################################################################
#   MAIL CONFIGURATION
####################################################################################################
# GMAIL CONFIGURATION
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'kpkmp34@gmail.com'
# EMAIL_HOST_PASSWORD = 'VIBER3880046'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# YAHOO CONFIGURATION
#EMAIL_HOST = 'smtp.mail.yahoo.com'
#If it first attempts to connect over IPv6 (and blocks for a few minutes) followed by a successful connection on IPv4
#This ensures that python will connect to gmail over IPv4 from the beginning !!!!

EMAIL_HOST = socket.gethostbyname('smtp.mail.yahoo.com')
EMAIL_HOST_USER = 'demodeya@yahoo.com'
EMAIL_HOST_PASSWORD = 'ipuvvkjkfdpfvpch'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DJANGO_SETTINGS_MODULE = 'deya.settings'