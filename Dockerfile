# Use Python slim image
FROM --platform=linux/amd64 python:3.12-slim

# Set working directory
WORKDIR /app

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the Flask app's port
EXPOSE 8080

# Set command to run the Flask app
CMD ["python", "app.py"]