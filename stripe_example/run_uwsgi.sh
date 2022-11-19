#!/usr/bin/env bash

chown www-data:www-data /var/log

sudo chown -R $USER $(pwd)

python3 manage.py collectstatic -c --no-input

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

python3 manage.py migrate

uwsgi --strict --ini /opt/app/movies_admin/uwsgi/uwsgi.ini