FROM python:3.9-slim

LABEL maintainer="jason@10layer.com"
LABEL version="1.0.0"
LABEL description="Sourcery NER API"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create model cache directory
RUN mkdir -p model_cache

# Expose the port (this is just documentation)
EXPOSE 8000

# Set default environment variables
ENV HOST=0.0.0.0
ENV PORT=8000

# Command to run the application
CMD ["python", "api.py"] 