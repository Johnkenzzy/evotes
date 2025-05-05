#!/bin/bash
set -e

DATA_DIR="/var/lib/postgresql/data"

# Initialize DB only if it hasn't been already
if [ ! -s "$DATA_DIR/PG_VERSION" ]; then
    echo "Initializing PostgreSQL data directory..."
    su - postgres -c "/usr/lib/postgresql/15/bin/initdb -D $DATA_DIR"
fi

# Start PostgreSQL in the background
echo "Starting PostgreSQL..."
su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D $DATA_DIR -l /tmp/logfile start"

# Wait until PostgreSQL is ready
until su - postgres -c "pg_isready -d postgres"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Run init.sql
echo "Running database initialization SQL script..."
su - postgres -c "psql -d postgres -f /evotes/init.sql"

# Stop PostgreSQL (optional, if you want supervisord to start it cleanly)
echo "Stopping PostgreSQL temporarily..."
su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D $DATA_DIR -m fast stop"

# Start supervisord (to manage both Django and PostgreSQL)
echo "Starting supervisord..."
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
