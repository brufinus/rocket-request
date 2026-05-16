#!/bin/bash
# Runs code scanning tools on Python files in the index and working tree.

pylint $(git ls-files '*.py')
coverage run -m pytest
coverage report -m
coverage html
