# Use a lightweight Ubuntu 22.04 base image
FROM python:3.11-slim

# Install Python 3.11 and pip
RUN apt-get update && \
    apt-get install -y python3.11 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install the required packages
COPY *.whl .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the application code and data to the container
COPY app_api_entrypoint.py app_api.py .env /app/

# Set the working directory to /app
WORKDIR /app

# EXPOSE 8046

# Start the application
CMD ["python3", "app_api_entrypoint.py"]
