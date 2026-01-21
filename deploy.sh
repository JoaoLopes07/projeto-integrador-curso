#!/usr/bin/env bash

set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput  # Add this line
python manage.py migrate --noinput