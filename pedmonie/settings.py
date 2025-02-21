"""
Django settings for pedmonie project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import environ
from pathlib import Path
from datetime import timedelta
import os
from decouple import config







# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY', default='fallback-secret-key')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['pedmonie-django-backend.onrender.com', '127.0.0.1', 'pedmonie-pedmonie.b.aivencloud.com']


# Application definition
# add django rest framework app
# add django rest framework-simplejwt app to enable JWT authentication

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',  # JWT Authentication !!! Do not edit
    'authentication',
    'dashboard',
    'wallets',
    'orders',
    'corsheaders',
    'payments',
    'support',
    'transactions',

]

# custom user model setting
AUTH_USER_MODEL = 'authentication.Merchant'

MIDDLEWARE = [
    
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'pedmonie.urls'

# configure django rest framework settings
# use JWT authentication for API requesrs
# require authentication for all views by default
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning', # request.version should return 1
    'DEFAULT_VERSION': 'v1', # DRF expects version numbers without prefixes e.g. 'v', else it would duplicate into /api/vv1/
    'ALLOWED_VERSIONS': ['v1'],
    'VERSION_PARAM': 'version',
}



SIMPLE_JWT = {
    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.CustomTokenObtainPairSerializer",
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False, # don't provide a new refresh JWT at the refresh endpoint
    "BLACKLIST_AFTER_ROTATION": True, # invalidate old refresh tokens
    # disable last login after token refresh as users abusing the views could slow the server, 
    # - creating a security risk e.g. DoS attack
    # - (set True if throttling is set)
    "UPDATE_LAST_LOGIN": False, 
    "SIGNING_KEY": config('JWT_SECRET_KEY', default=None), # Django secret is backup
    "ALGORITHM": "HS256", # defaults to using 256-bit HMAC signing
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "merchant_id", # use merchant_id instead of id
    "USER_ID_CLAIM": "merchant_id", # use merchant_id in the token claims
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",), # specify that JWT is used for authorisation
}

# raise an error if there is no JWT_SECRET_KEY
# use `python -c "import secrets; print(secrets.token_hex(32))"` command & save it to .env
if SIMPLE_JWT["SIGNING_KEY"] is None:
    raise ValueError("JWT_SECRET_KEY is not set in the environment variables.") 

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

WSGI_APPLICATION = 'pedmonie.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),  # Change to your DB name in .env file
        'USER': config('DB_USER'),         # Change to your MySQL username in .env file
        'PASSWORD': config('DB_PASSWORD'),  # Change to your MySQL password in .env file
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'



# https://help.pythonanywhere.com/pages/DjangoStaticFiles#set-static_root-in-settingspy
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# more places for collectstatic to find static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# whitenoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# create an empty static directory if it does not exist
if not os.path.exists(os.path.join(BASE_DIR, 'static')):
    os.makedirs(os.path.join(BASE_DIR, 'static'))

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Redis settings
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_DB = config('REDIS_DB')
REDIS_USERNAME = config('REDIS_USERNAME')
REDIS_PASSWORD = config('REDIS_PASSWORD')



CACHES = {
    "default": {
        "BACKEND": config('REDIS_CACHE_BACKEND'),
        "LOCATION": config('REDIS_CACHE_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}




EMAIL_VERIFICATION_TIMEOUT = config('EMAIL_VERIFICATION_TIMEOUT') 
VERIFICATION_CODE_LENGTH = config('VERIFICATION_CODE_LENGTH')


EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
EMAIL_USE_TLS = False
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
FROM_EMAIL = config('FROM_EMAIL')

FRONTEND_URL = config('FRONTEND_URL')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'django.mail': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    "https://pedmonie-django-backend.onrender.com"
]

