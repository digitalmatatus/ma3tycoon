#!/bin/bash

NAME="ma3tycoon_app"                                   # Name of the application
DJANGODIR=/home/digim/ma3tycoon               # Django project directory
SOCKFILE=/home/digim/ma3tycoon/venv/run/gunicorn.sock  # we will communicte using this unix socket
USER=digim                                         # the user to run as
GROUP=digim                                        # the group to run as
NUM_WORKERS=3                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=ma3tycoon.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=ma3tycoon.wsgi              # WSGI module name
echo "Starting $NAME as `whoami`"

# Activate the virtual environment

cd $DJANGODIR
source /home/digim/ma3tycoon/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=- \
  --limit-request-line 8190

