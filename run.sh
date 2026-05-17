#!/bin/bash
# =============================================================
# run.sh
#
# Description:
#  Automates various processes for development. 
#
# Usage:
#   ./run.sh [-b] [-i] [-m] [-s] [-S]
#
# Flags:
#   -b  Build the distribution.
#   -i  Install the app.
#   -m  Migrate models.
#   -s  Run the dev server.
#   -S  Perform all the above steps.
#
# Dependencies:
#   Installed build and other requirements in requirements.txt.
#
# Author: Bernard Rufinus
# Date: 2026/05/17
# =============================================================

function build {
    python -m build django-distribute
}

function install {
    pip install django-distribute/dist/django_distribute-*.tar.gz
}

function migrate {
    python django-rocket-request/manage.py migrate
}

function runServer {
    python django-rocket-request/manage.py runserver
}

function printUsage {
    echo "Usage:"
    flags=(
        'b: Build the distribution.'
        'i: Install the app.'
        'm: Run migrations.'
        's: Run the dev server.'
        'S: Build and install, then run the dev server.'
    )
    for flag in "${flags[@]}"; do
        printf "\t-%s\n" "$flag"
    done
}

function main {
    # Entry point that parses flags and calls appropriate functions.
    if [[ $# -eq 0 ]]; then
        printUsage
        exit 1
    fi
    if [[ "$*" == *"-A"* ]]; then
        doAll
        exit 0
    fi
    while getopts 'bimsS' flag; do
        case "${flag}" in 
            b) build ;;
            i) install ;;
            m) migrate ;;
            s) runServer ;;
            S) build; install; migrate; runServer ;;
            *) printUsage
                exit 1 ;;
        esac
    done
}

main "$@"
