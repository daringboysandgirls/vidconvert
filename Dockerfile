FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]