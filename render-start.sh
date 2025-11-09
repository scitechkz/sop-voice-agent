#!/usr/bin/env bash
#This file needs to be made executable to run: chmod +x render-start.sh
# 1. Ensure the secrets directory exists
mkdir -p /etc/secrets

# 2. Decode the Base64 credential and save it as a JSON file
echo "$GOOGLE_CREDENTIALS_BASE64" | base64 -d > /etc/secrets/google_credentials.json

# 3. Start the Gunicorn/Uvicorn server
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:$PORT