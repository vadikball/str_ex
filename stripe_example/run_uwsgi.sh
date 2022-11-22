#!/usr/bin/env bash

chown www-data:www-data /var/log

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

uwsgi --strict --ini /stripe_example/uwsgi/uwsgi.ini