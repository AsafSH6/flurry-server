#!/bin/bash

APPNAME="flurry"
APPDIR=/home/ubuntu/$APPNAME/
USER=ubuntu
ADDRESS="0.0.0.0:8001"
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=$APPNAME.settings
DJANGO_WSGI_MODULE=$APPNAME.wsgi

echo "Starting $APPNAME as `whoami`"

cd $APPDIR

export DJANGO_SETTING_MODULE=$DJANGO_SETTING_MODULE


exec gunicorn ${DJANGO_WSGI_MODULE}:application \
 --name $APPNAME \
 --workers $NUM_WORKERS \
 --user $USER \
 --bind=$ADDRESS \
 --log-level=debug \
# --log-file=$APPDIR"logs/gunicorn.log"
 --log-file=-
