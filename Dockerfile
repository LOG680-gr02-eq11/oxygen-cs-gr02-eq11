# Use Python Alpine as base image for building
FROM python:3.8-alpine

# Define working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Start application
CMD ["python", "src/main.py"]
