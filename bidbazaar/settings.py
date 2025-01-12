

from pathlib import Path
from celery.schedules import crontab
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3lk(rwa$u9m_s@uz3nkqzn#i%kg!y&!6d)3wjso0tytfq8t190'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'product',
    'coin_purchase',
    'BidPlacement',
    'rewards'



]
ASGI_APPLICATION = 'bidbazaar.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bidbazaar.urls'

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

WSGI_APPLICATION = 'bidbazaar.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bidbazaaar',
        'USER': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    'bidbazaar/static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "Danger",

}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'uk200114@gmail.com'
EMAIL_HOST_PASSWORD = 'rvfu iszz saja ieyj'


STRIPE_SECRET_KEY = 'sk_test_51PXqdvHxKAFHWD8vLoYYpC6HWhfd9KNoeI3IvPTMJSvAsavX8bvISVRWpPJV8YTCgSUW2zoy2E9bFF2EPwRtTNCP00rQpzvws7'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51PXqdvHxKAFHWD8vrsMTEtXTwlQmMM2kQHBOvBK3wkhsO6tc1zh5NxQELoO2HxSlg9au0VQD9FkMSYI4eB3SBR6Z001NRyxniX'



TIME_ZONE = 'Asia/Karachi'
USE_TZ = True






DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




CELERY_BROKER_URL = 'redis://localhost:6379/0'


CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


CELERY_TIMEZONE = 'UTC'


CELERY_BEAT_SCHEDULE = {
    'ai-bid-task': {
        'task': 'bidplacement.tasks.ai_place_bids',
        'schedule': crontab(minute='*/1'),
    },
}
