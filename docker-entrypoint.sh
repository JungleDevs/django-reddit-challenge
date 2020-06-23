#!/bin/bash
set -e

if [ "$1" = "manage" ]; then
    shift 1
    exec python manage.py "$@"
else
    python manage.py migrate                  # Apply database migrations
    python manage.py collectstatic --noinput  # Collect static files

    # Prepare log files and start outputting logs to stdout
    touch /usr/src/logs/gunicorn.log
    touch /usr/src/logs/access.log
    tail -n 0 -f /usr/src/logs/*.log &

    # Start Gunicorn processes
    echo Starting Gunicorn.
    exec gunicorn settings.wsgi \
        --name backend-challenge-001-django \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120 \
        --log-level=info \
        --log-file=/usr/src/logs/gunicorn.log \
        --access-logfile=/usr/src/logs/access.log \
        "$@"
fi
