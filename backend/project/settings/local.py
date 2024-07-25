"""
Django settings for local environment.
"""

from django.utils.log import DEFAULT_LOGGING
import logging.config
import logging
from datetime import timedelta
from pathlib import Path
from project.settings import get_secret
from typing import Dict, Tuple, List, Any, Union
from django.utils.translation import gettext_lazy as _
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = get_secret('SECRET_KEY', 'your_secret_key')

DEBUG = True

ALLOWED_HOSTS: List[str] = []

INSTALLED_APPS: List[str] = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'corsheaders',
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


JWT_AUTH: Dict[str, Any] = {
    'JWT_SECRET_KEY': 'your_jwt_secret_key',
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_DELTA': timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}

MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'authentication.middlewares.locale_middleware.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]


CORS_ALLOW_ALL_ORIGINS: bool = False
CORS_ALLOWED_ORIGINS: list[str] = [
    "http://localhost:3000",
]


CORS_ALLOW_CREDENTIALS: bool = True
CORS_ALLOW_HEADERS: list[str] = [
    'content-type',
    'x-csrftoken',
]

CSRF_TRUSTED_ORIGINS: list[str] = [
    "http://localhost:3000",
]

SESSION_ENGINE: str = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME: str = 'sessionid'
SESSION_COOKIE_SECURE: bool = False
SESSION_EXPIRE_AT_BROWSER_CLOSE: bool = False
SESSION_COOKIE_HTTPONLY: bool = True

LANGUAGE_CODE: str = 'en'

LANGUAGES: List[tuple[str, str]] = [
    ('en', _('English')),
    ('sv', _('Swedish'))
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGE_COOKIE_NAME: str = 'language_code'

ROOT_URLCONF: str = 'project.urls'

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

WSGI_APPLICATION: str = 'project.wsgi.application'

DATABASES: Dict[str, Dict[str, str | None]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret("POSTGRES_NAME"),
        'USER': get_secret("POSTGRES_USER"),
        'PASSWORD': get_secret("POSTGRES_PASSWORD"),
        'HOST': get_secret("POSTGRES_HOST"),
        'PORT': get_secret("POSTGRES_PORT"),
    }
}

TIME_ZONE: str = 'UTC'

USE_I18N: bool = True

USE_TZ: bool = True

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

CACHES: Dict[str, dict[str, str]] = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

BANKID: Dict[str, str | None] = {
    "endpoint": get_secret('BANKID_ENDPOINT'),
    "ca_cert_path": get_secret('BANKID_CA_CERT'),
    "cert_path": get_secret('BANKID_CERT_PEM_PATH'),
    "cert_key_path": get_secret('BANKID_CERT_PEM_KEY_PATH'),
}

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
