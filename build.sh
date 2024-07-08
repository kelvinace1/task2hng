#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e


# Corrected path with backslashes for Windows


# Initialize and update git submodules (if any)
export DJANGO_SETTINGS_MODULE=hngorg.settings.production


echo "building the project"
pip install -r requirements.txt

echo "make migrations..."
echo "hope"
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "collect static..."
python manage.py collectstatic --noinput --clear
