#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py load_allowed_voters
python manage.py load_candidates
python manage.py createsuperuser --noinput || true