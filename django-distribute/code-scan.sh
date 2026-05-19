#!/bin/bash
# Runs local code scanning tools on the app.

pylint --load-plugins=pylint_django --ignore tests .

coverage run runtests.py
coverage report -m
coverage html
