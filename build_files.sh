#!/bin/bash

# Build the project
echo "Building the project..."
python3 -m pip install -r requirements.txt

echo "Collect Static..."
python manage.py collectstatic --noinput --clear

mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/
