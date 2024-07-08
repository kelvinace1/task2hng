#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e
set -x

source C:\Users\USER\hngorg/venv/bin/activate 
# Initialize and update git submodules (if any)
export DJANGO_SETTINGS_MODULE=hngorg.settings.production

git submodule init
git submodule update

echo "building the project"
pip install -r requirements.txt

echo "make migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "collect static..."
python manage.py collectstatic --noinput --clear
