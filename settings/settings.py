"""
backend-challenge-001 settings
"""
###
# Libraries
###
import os
import requests

import dj_database_url
import dotenv
import sentry_sdk

from s3_environ import S3Environ
from sentry_sdk.integrations.django import DjangoIntegration

###
# Get data from .env file
###
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.read_dotenv(os.path.join(BASE_DIR, '.env'))
ENVIRONMENT = os.environ.get('ENVIRONMENT')
LOAD_ENVS_FROM_FILE = True if os.environ.get('LOAD_ENVS_FROM_FILE', False) == 'True' else False

env_file = 'envs-production.json' if ENVIRONMENT == 'production' else 'envs-staging.json'
if not LOAD_ENVS_FROM_FILE:
    S3Environ(bucket='bucket-env', key=env_file)
    print("Loading envs from S3: {0}".format(env_file))

###
# Security
###
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = ENVIRONMENT == 'development' or os.environ.get('DEBUG', False)

ALLOWED_HOSTS = [
    '.us-west-2.elb.amazonaws.com',
    '.compute-1.amazonaws.com',
    'localhost',
]

EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get(
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        timeout=0.01,
    ).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

###
# Application definition
###
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Rest Framework
    'rest_framework',
    'rest_framework.authtoken',

    # Storage
    'storages',

    # Rest Auth
    'rest_auth',
    'rest_auth.registration',

    # Allauth
    'allauth',
    'allauth.account',

    # Social Applications
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # Cors
    'corsheaders',

    # Applications
    'accounts',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

###
# Database
###
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
DATABASES['default']['ATOMIC_REQUESTS'] = True

###
# Internationalization
###
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

###
# Static Files
###
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

###
# Storage
###
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True
AWS_IS_GZIPPED = True
AWS_QUERYSTRING_AUTH = False
if DEBUG or ENVIRONMENT == 'test':
    AWS_S3_ENDPOINT_URL = 'http://localhost:4572/'
    AWS_SECRET_ACCESS_KEY = 'foo'
    AWS_ACCESS_KEY_ID = 'foo'

###
# Rest Framework
###
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

###
# Authentication
###
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'accounts.api.v1.serializers.UserTokenSerializer',
    'PASSWORD_RESET_SERIALIZER': 'accounts.api.v1.serializers.PasswordResetSerializer',
}

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_ADAPTER = os.environ.get('ACCOUNT_ADAPTER', 'allauth.account.adapter.DefaultAccountAdapter')
SOCIALACCOUNT_EMAIL_VERIFICATION = os.environ.get('SOCIALACCOUNT_EMAIL_VERIFICATION', 'none')

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': [
            'email',
            'public_profile',
            'user_friends',
            'user_birthday',
        ],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
            'location',
            'birthday',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.8',
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
}

###
# Change Password
###
OLD_PASSWORD_FIELD_ENABLED = True

###
# CORS
###
CORS_ORIGIN_ALLOW_ALL = True

###
# Sentry & Logging
###
if not DEBUG and ENVIRONMENT != 'test':
    def before_send(event, hint):
        # Ignore disallowed hosts
        if event.get('logger') == 'django.security.DisallowedHost':
            return None
        return event

    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        before_send=before_send,
    )


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry': {
            'level': 'ERROR',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', ],
            'propagate': False,
        },
        'amazon-logs': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
}

###
# FE Settings
###
FE_URL = os.environ.get('FE_URL')

###
# Email Backend
###
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
if not DEBUG and ENVIRONMENT != 'test':
    EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
    AWS_DEFAULT_REGION = 'us-west-2'
