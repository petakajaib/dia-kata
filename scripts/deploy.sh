#!/bin/bash

NAME="extracting_talker_api"
DIR=/home/urban/extracting-talker
USER=th3go2
GROUP=th3go2
WORKERS=8
BIND=unix:/home/th3go2/extracting-talker/gunicorn.sock
LOG_LEVEL=info

cd $DIR
source venv/bin/activate
export APP_ENVIRONMENT=production
exec venv/bin/gunicorn flask_app:app \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-