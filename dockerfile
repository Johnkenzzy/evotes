FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /evotes

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv or requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Copy and make entrypoint script executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint script to wait for DB before starting
ENTRYPOINT ["/entrypoint.sh"]

# Gunicorn start command (used by Railway/Nixpacks)
CMD ["gunicorn", "backend.config.wsgi:application", "--bind", "0.0.0.0:8000"]
