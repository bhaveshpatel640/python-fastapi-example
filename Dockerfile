# Use the official Python image as the base image
FROM public.ecr.aws/docker/library/python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and create a non-root user
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    useradd --create-home appuser

# Switch to the non-root user
USER appuser

# Copy only the requirements file to leverage Docker's cache
COPY requirements.txt ./

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--port", "8000", "--host", "0.0.0.0"]