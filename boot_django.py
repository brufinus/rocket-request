"""Sets up a Django environment to run commands against."""

import sys
from pathlib import Path
import django
from django.conf import settings

BASE_DIR = Path(__file__).parent / "django_distribute"
sys.path.insert(0, str(BASE_DIR))


def boot_django():
    """Configure and set up Django."""
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        ALLOWED_HOSTS=("*"),
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        },
        SECRET_KEY="django-insecure-$4gbgz8ea%peul=b!2d3oj3ln3j(ar$t1uccym+p@jhp))rt_8",
        STATIC_URL="/static/",
        ROOT_URLCONF="django_distribute.tests.urls",
        INSTALLED_APPS=(
            "django_distribute",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ),
        MIDDLEWARE=(
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ),
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                        "django_distribute.context_processors.build_date",
                        "django_distribute.context_processors.build_version",
                    ],
                },
            },
        ],
        SESSION_ENGINE="django.contrib.sessions.backends.signed_cookies",
    )
    django.setup()
