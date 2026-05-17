#!/bin/bash
# Builds and installs django_distribute, then runs the local development server.

python -m build django-distribute
pip install django-distribute/dist/django_distribute-*.tar.gz
python django-rocket-request/manage.py runserver
