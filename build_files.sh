#!/bin/bash

# Build the project
echo "Building the project..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Python version:"
python --version

echo "Collect Static..."
python manage.py collectstatic --noinput --clear

mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/
