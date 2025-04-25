# Use official Python image
FROM python:3.8

# Set work directory
WORKDIR /evotes/backend

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
