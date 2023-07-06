# Use Python image to build dependencies
FROM python:3.8 as builder

# Define working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use Distroless as final base
FROM gcr.io/distroless/python3-debian10

# Copy required files from builder
COPY --from=builder /app /app
COPY src/ /app/src/

# Define working directory
WORKDIR /app

# Start application
CMD ["python", "src/main.py"]
