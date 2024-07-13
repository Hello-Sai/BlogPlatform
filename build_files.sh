#!/bin/bash

echo "BUILD START"

# Install dependencies from requirements.txt
python -m pip install -r requirements.txt

# Collect static files (CSS, JS, images) into STATIC_ROOT
python manage.py collectstatic --noinput --clear

echo "BUILD END"
