#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e


# Corrected path with backslashes for Windows


# Initialize and update git submodules (if any)
source venv/bin/activate


echo "building the project"
echo "build"
python3 -m pip install -r requirements.txt

echo "make migrations..."
echo "hope"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "collect static..."
python3 manage.py collectstatic --noinput --clear
