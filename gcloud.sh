#!/bin/bash
# =============================================================
# gcloud.sh
#
# Description:
#  Automates various processes for gcloud deployment. 
#
# Usage:
#   ./run.sh [-b] [-d]
#
# Flags:
#   -b  Build the image.
#   -d  Deploy the image.
#
# Author: Bernard Rufinus
# Date: 2026/05/28
# =============================================================

REGION=us-central1
PROJECT_ID=rocket-request
SERVICE_NAME=distribute-service

function build {
    gcloud builds submit --config cloud_migrate.yml
}

function deploy {
    gcloud run deploy $SERVICE_NAME \
        --region $REGION \
        --image ${REGION}-docker.pkg.dev/$PROJECT_ID/cloud-run-source-deploy/$SERVICE_NAME \
        --service-account ${SERVICE_NAME}-account@${PROJECT_ID}.iam.gserviceaccount.com
}

function printUsage {
    echo "Usage:"
    flags=(
        'b: Build the image.'
        'd: Deploy the image.'
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
    while getopts 'bd' flag; do
        case "${flag}" in 
            b) build ;;
            d) deploy ;;
            *) printUsage
                exit 1 ;;
        esac
    done
}

main "$@"
