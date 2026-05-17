#!/bin/bash
# Runs local code scanning tools on the app.

pylint --ignore tests .

coverage run runtests.py
coverage report -m
coverage html
