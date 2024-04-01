"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta

from django.conf import settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "rand0m&k3yF0R-someus3"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "true").lower() == "true"

DEBUG = True

if not DEBUG:
    # Sentry will only be enabled if the debug flag is FALSE, as it
    # should run only to listen to production problems to avoid wasting
    # credits and throwing known errors.
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(os.environ.get("SENTRY_DSN"), integrations=[DjangoIntegration()])

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    # Miscellaneous
    "storages",
    "django_filters",
    "nested_admin",
    "django_celery_results",
    # Module
    "common",
    "user",
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "widget_tweaks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.logger.RequestLogMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRESQL_ADDON_DB", "base"),
        "USER": os.environ.get("POSTGRESQL_ADDON_USER", "base"),
        "PASSWORD": os.environ.get("POSTGRESQL_ADDON_PASSWORD", "base"),
        "HOST": os.environ.get("POSTGRESQL_ADDON_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRESQL_ADDON_PORT", 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] - {asctime} : {message}",
            "style": "{",
        }
    },
    "filters": {"not_found_filter": {"()": "app.filter.NotFoundFilter"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    # This is the HTTP logger
    "loggers": {
        "django.server": {
            "handlers": ["console"],
            "filters": ["not_found_filter"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "filters": ["not_found_filter"],
            "propagate": False,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# LANGUAGES = [("en", "English"), ("fr", "French")]
#
# LOCALE_PATHS = (
#     os.path.join(os.path.normpath(BASE_DIR + os.sep + os.pardir), "locale"),
# )


STATIC_ROOT = os.path.join(BASE_DIR, "..", "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

print("STEVE: STATIC_ROOT:" + str(STATIC_ROOT))
print("STEVE: STATICFILES_DIRS:" + str(STATICFILES_DIRS))

MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")
MEDIA_URL = "/media/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Celery + redis
CELERY_QUEUE = os.environ.get("CELERY_QUEUE", "celery")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = "django-db"

# django auth
AUTH_USER_MODEL = "user.CustomUser"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/auth/profile/"

OBJECTS_PER_PAGE = 25

# django all auth
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"


# Prevent warning
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
