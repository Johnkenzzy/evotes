FROM python:3.12-slim

# Install PostgreSQL and other dependencies
RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib \
    libpq-dev gcc netcat-openbsd supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create postgres data directory
RUN mkdir -p /var/lib/postgresql/data /run/postgresql && \
    chown -R postgres:postgres /var/lib/postgresql /run/postgresql

# Set work directory
WORKDIR /evotes

# Copy app code
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Entrypoint script
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
