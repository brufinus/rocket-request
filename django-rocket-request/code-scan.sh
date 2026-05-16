#!/bin/bash
# Runs code scanning tools on Python files in the index and working tree.

pylint .
coverage run --source='.' manage.py test django_distribute
coverage report -m
coverage html
