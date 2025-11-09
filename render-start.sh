#!/usr/bin/env bash

# Start the Gunicorn/Uvicorn server
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:$PORT