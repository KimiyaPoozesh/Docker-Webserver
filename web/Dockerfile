# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Update and install necessary packages
RUN apt-get update -o Acquire::Check-Valid-Until=false \
    && apt-get install -y build-essential

# Create and set the working directory
RUN mkdir /code
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project code
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Command to run Django app with uWSGI
CMD ["uwsgi", "--http", "0.0.0.0:8000", "--module", "myproject.wsgi:application", "--master", "--processes", "4", "--threads", "2"]
