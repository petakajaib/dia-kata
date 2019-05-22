#!/bin/bash

export APP_ENVIRONMENT=development

gunicorn flask_app:app --reload --bind 0.0.0.0
