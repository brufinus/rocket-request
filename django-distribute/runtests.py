#!/usr/bin/env python
"""Runs tests for django_distribute."""

# pylint: disable=invalid-name

import argparse
import multiprocessing
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def parse_args():
    """Parses arguments for the test runner."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", action="append", dest="tags", default=[])
    parser.add_argument(
        "--exclude-tag", action="append", dest="exclude_tags", default=[]
    )
    parser.add_argument("-p", action="store_true", dest="parallel")
    return parser.parse_args()


def runtests():
    """Configure settings and run tests."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

    args = parse_args()
    parallel = 0
    if args.parallel:
        parallel = multiprocessing.cpu_count()

    django.setup()
    runner = get_runner(settings)
    test_runner = runner(
        interactive=False,
        failfast=False,
        tags=args.tags,
        exclude_tags=args.exclude_tags,
        parallel=parallel,
    )
    failures = test_runner.run_tests(["django_distribute"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests()
