#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn processes
exec gunicorn cybercamp_backoffice.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3
