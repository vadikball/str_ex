#!/usr/bin/env bash

sudo chown -R $USER $(pwd)

python3 manage.py collectstatic -c --no-input