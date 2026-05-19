#!/usr/bin/env python
"""Runs tests for django_distribute."""

# pylint: disable=invalid-name
# pylint: disable=django-not-configured

import argparse
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def runtests():
    """Parse arguments for tags, configure settings, and run tests."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", action="append", dest="tags", default=[])
    parser.add_argument(
        "--exclude-tag", action="append", dest="exclude_tags", default=[]
    )
    args = parser.parse_args()

    if not settings.configured:
        DATABASES = {
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        }

        settings.configure(
            DATABASES=DATABASES,
            SECRET_KEY="django-insecure-$4gbgz8ea%peul=b!2d3oj3ln3j(ar$t1uccym+p@jhp))rt_8",
            STATIC_URL="static/",
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
                        ],
                    },
                },
            ],
            MIGRATION_MODULES={"distribute": None},
        )

    django.setup()
    runner = get_runner(settings)
    test_runner = runner(
        interactive=False,
        failfast=False,
        tags=args.tags,
        exclude_tags=args.exclude_tags,
    )
    failures = test_runner.run_tests(["django_distribute"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests()
