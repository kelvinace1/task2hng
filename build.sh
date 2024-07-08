#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

# Initialize and update git submodules (if any)
git submodule init
git submodule update

echo "building the project"
pip install -r requirements.txt

echo "make migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "collect static..."
python manage.py collectstatic --noinput --clear
