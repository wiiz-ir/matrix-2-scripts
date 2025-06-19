#!/bin/bash

# Define variables
SERVER="V_SERVER_USERNAME@V_SERVER_ADDRESS"
SSH_KEY="V_KEY_PATH"
SOURCE_DIR="V_PROJECT_SOURCE_DIR"
DEST_DIR="V_PROJECT_DEST_DIR"

# Execute rsync command
rsync -avz \
    --exclude 'edge/acme.json' \
    --exclude 'commands.md' \
    --exclude 'README.md' \
    --exclude '.vscode' \
    --exclude '.venv' \
    --exclude 'deploy.sh' \
    --exclude 'src' \
    --exclude '.git' \
    -e "ssh -i ${SSH_KEY}" \
    "${SOURCE_DIR}" \
    "${SERVER}:${DEST_DIR}"