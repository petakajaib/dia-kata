#!/bin/bash

source venv/bin/activate
export APP_ENVIRONMENT=development

gunicorn flask_app:app --reload
