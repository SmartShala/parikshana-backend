"""
Django settings for parikshana project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from typing import List, Tuple

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("debug", 0) == "1"

ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = "user.User"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "storages",
    "silk",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_minio_backend",
    "corsheaders",
    "django_filters",
    "import_export",
    "grader_app",
    "test_app",
    "user",
    "school_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "silk.middleware.SilkyMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "parikshana.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "parikshana.wsgi.application"

LOGIN_URL = "/api/admin/login"
LOGOUT_URL = "/api/admin/logout"
BASE_URL = os.getenv("base_url")

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("postgres_db"),
        "USER": os.getenv("postgres_user"),
        "PASSWORD": os.getenv("postgres_password"),
        "HOST": "postgres",
        "PORT": 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        # "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_RENDERER_CLASSES": [
        # "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "parikshana.custom_paginator.CustomPagination",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# Default primary key field type
# https://doc   s.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SILK
SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True

# CELERY SETTINGS
CELERY_BROKER_URL = f'redis://{os.getenv("redis_username")}:{os.getenv("redis_password")}@{os.getenv("redis_host")}:{os.getenv("redis_port")}'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True

# Minio

MINIO_PRIVATE_BUCKETS = ["parikshana-media", "parikshana-static"]
MINIO_PUBLIC_BUCKETS = []

STATICFILES_STORAGE = "django_minio_backend.models.MinioBackendStatic"
DEFAULT_FILE_STORAGE = "django_minio_backend.models.MinioBackend"

MINIO_ENDPOINT = os.getenv("minio_internal_endpoint")
MINIO_EXTERNAL_ENDPOINT = os.getenv("minio_external_endpoint")
MINIO_ACCESS_KEY = os.getenv("minio_key")
MINIO_SECRET_KEY = os.getenv("minio_secret")
MINIO_URL_EXPIRY_HOURS = timedelta(days=1)  # Default is 7 days (longest) if not defined
MINIO_CONSISTENCY_CHECK_ON_START = True
MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = False
MINIO_USE_HTTPS = False
MINIO_POLICY_HOOKS: List[Tuple[str, dict]] = []
MINIO_MEDIA_FILES_BUCKET = "parikshana-media"  # replacement for MEDIA_ROOT
MINIO_STATIC_FILES_BUCKET = "parikshana-static"  # replacement for STATIC_ROOT
MINIO_BUCKET_CHECK_ON_SAVE = (
    True  # Default: True // Creates bucket if missing, then save
)


# SWAGGER
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "SECURITY_DEFINITIONS": {
        "basic": {"type": "basic"},
        "apiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Bearer {token}",
        },
    },
    "DOC_EXPANSION": "none",
    "OPERATIONS_SORTER": "alpha",
}
