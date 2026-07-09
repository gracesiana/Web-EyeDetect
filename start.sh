#!/usr/bin/env bash
set -e

cd backend

echo "Running database migrations..."
python manage.py migrate

echo "Ensuring default admin accounts..."
python manage.py ensure_default_admin

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn EyeDetect.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
