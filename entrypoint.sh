#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "PostgreSQL is up - continuing..."

# Optional: Run migrations and collect static files
python backend/manage.py migrate --noinput
python backend/manage.py collectstatic --noinput

# Start the application
exec gunicorn backend.config.wsgi:application --bind 0.0.0.0:8000
