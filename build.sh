#!/usr/bin/env bash
# exit on error
set -o errexit

# install dependencies
pip install -r requirements.txt

# install the project
python manage.py collectstatic --no-input
python manage.py migrate