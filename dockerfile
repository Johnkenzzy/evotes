# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /evotes

# Install system dependencies
RUN apt-get update && apt-get install -y netcat gcc postgresql-client && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy project
COPY . .

# Make entrypoint script executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8000

# Start server
CMD ["sh", "./entrypoint.sh"]
