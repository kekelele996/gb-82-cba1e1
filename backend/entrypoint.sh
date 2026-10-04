#!/bin/bash
set -e

echo "Migrating database..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding initial data..."
python seeders/seed_data.py

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
