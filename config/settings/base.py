from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "organizations",
    "pages",
    "parameters",
    "django_extensions",
    "simple_history",
    "tailwind",
    "theme",
]

TAILWIND_APP_NAME = "theme"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom context processor for organization, contacts, tasks and day off count
                "apps.organizations.context_processor.organization_count",
                "apps.organizations.context_processor.org_employees_count",
                "apps.organizations.context_processor.user_work_time",
            ],
        },
    },
]

AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DEFAULT_FROM_EMAIL = "admin@acsservices.gr"

LOGIN_URL = "login"

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Athens"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
