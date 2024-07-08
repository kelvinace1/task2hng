#!/bin/bash

echo "building the project"
pip install -r requirements.txt

echo "make migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "collect static..."
python manage.py collectstatic --noinput --clear
