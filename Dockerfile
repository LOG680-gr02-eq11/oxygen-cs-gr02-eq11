# Use Python Alpine as base image
FROM python:3.8-alpine as builder

# Define working directory
WORKDIR /app

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Install build dependencies and pipenv
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies with pipenv
RUN pipenv install --system --deploy && \
    apk del .build-deps

# Runtime Image
FROM python:3.8-alpine

# Define working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application files
COPY . /app

# Expose the port your app listens on
EXPOSE 80

# Start application
CMD ["pipenv", "run", "start"]
