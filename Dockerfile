# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
RUN mkdir /code
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the entire project code
COPY . /code/

# Install gunicorn
RUN pip install gunicorn

# Expose port 8000
EXPOSE 8000

# Command to run Django app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
