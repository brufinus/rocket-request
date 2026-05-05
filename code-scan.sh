#!/bin/bash
# Runs code scanning tools on Python files in the index and working tree.

pytest
pylint $(git ls-files '*.py')
coverage run -m pytest
coverage report -m
coverage html
