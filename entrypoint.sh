#!/bin/sh

sleep 10  # TODO: better solution

python manage.py migrate

python seed_db.py  // for testing purposes

exec python manage.py runserver ${DJANGO_HOST}:${DJANGO_PORT}