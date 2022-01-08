#!/bin/bash

set -euo pipefail

cmd="$1"
shift

case $cmd in

  devserver)
    set -x
    exec ./manage.py runserver 0:$PORT
    ;;

  prodserver)
    set -x
    exec gunicorn --bind 0:$PORT --workers 4 geospatial.wsgi:application
    ;;

  *)
    echo "Unknown command $cmd"
    exit 1
    ;;

esac
