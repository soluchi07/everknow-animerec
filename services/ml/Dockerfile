# Use a Python base image, preferably one for data science (slim is often enough)
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install the necessary dependencies for all ML and ETL scripts
# We are assuming a single requirements.txt for simplicity, but 
# you might need to create a dedicated ml_requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint is not strictly necessary as we are using 'tail -f /dev/null' 
# in the docker-compose command, but often included for standard practice.
# ENTRYPOINT ["python"]