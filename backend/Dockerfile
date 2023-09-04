# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install system dependencies and the packages specified in requirements.txt
RUN apt update && \
    apt install --yes zbar-tools poppler-utils && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Set environment variables
ENV PORT 8080
ENV HOST 0.0.0.0

# Expose the port the application runs on
EXPOSE $PORT

# Start the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
