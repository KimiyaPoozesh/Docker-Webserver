# Use the official NGINX image from the Docker Hub
FROM nginx:latest

# Copy custom NGINX config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static files
COPY /html /usr/share/nginx/html
