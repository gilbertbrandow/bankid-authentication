"""
Django settings for local environment.
"""

from pathlib import Path
from project.settings import get_secret
from typing import Dict, Tuple, List, Any, Union

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = get_secret('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS: List[str] = ['*']

INSTALLED_APPS: List[str] = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'rest_framework',
    'authentication',
]

REST_FRAMEWORK: Dict[str, Union[Tuple[str, ...], str]] = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.jwt_authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'authentication.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'UNAUTHENTICATED_USER': 'authentication.models.CustomAnonymousUser',
}

from datetime import timedelta

JWT_AUTH: Dict[str, Any] = {
    'JWT_SECRET_KEY': 'your_jwt_secret_key',
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_DELTA': timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}

MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret("POSTGRES_NAME"),
        'USER': get_secret("POSTGRES_USER"),
        'PASSWORD': get_secret("POSTGRES_PASSWORD"),
        'HOST': get_secret("POSTGRES_HOST"),
        'PORT': get_secret("POSTGRES_PORT"),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import logging
import logging.config
from django.utils.log import DEFAULT_LOGGING

LOGGING: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Optionally disable file watching logs if possible
DEFAULT_LOGGING['handlers']['console']['level'] = 'ERROR'
logging.config.dictConfig(DEFAULT_LOGGING)
