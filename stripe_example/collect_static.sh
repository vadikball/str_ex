#!/usr/bin/env bash

chown -R $USER $(pwd)

python3 manage.py collectstatic -c --no-input