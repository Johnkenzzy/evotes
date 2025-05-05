FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /evotes

# Copy app code
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Gunicorn start command
CMD ["gunicorn", "evotes.wsgi:application", "--bind", "0.0.0.0:8000"]
