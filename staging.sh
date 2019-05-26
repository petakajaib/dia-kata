#!/bin/bash

source venv/bin/activate
export APP_ENVIRONMENT=staging

gunicorn flask_app:app --reload --bind 0.0.0.0
