#!/bin/sh

sleep 10  # TODO: better solution

python manage.py migrate

exec python manage.py runserver ${DJANGO_HOST}:${DJANGO_PORT}