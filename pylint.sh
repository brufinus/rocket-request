#!/bin/bash
# Runs pylint on Python files in the index and working tree.

pylint $(git ls-files '*.py')
