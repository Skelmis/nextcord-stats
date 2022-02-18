#!/bin/bash
touch /var/log/gunicorn.log
touch /var/log/gunicorn-access.log
tail -n 0 -f /var/log/gunicorn*.log &

python manage.py migrate
exec gunicorn nextcord_stats.wsgi:application -c gunicorn.conf.py