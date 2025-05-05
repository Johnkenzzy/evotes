#!/bin/sh
set -e

echo "Waiting for PostgreSQL at $PGHOST:$PGPORT..."

# Wait for DB to be ready
while ! nc -z $PGHOST $PGPORT; do
  sleep 1
done

echo "PostgreSQL is up - running migrations..."

# Run DB migrations and collect static files
python backend/manage.py migrate --noinput

# Launch gunicorn server
exec "$@"