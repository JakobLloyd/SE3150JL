# Use an official Python image as the base
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy application files into the container
COPY . /app

# Expose the ports for both servers
EXPOSE 8080 8000

# Run both the squirrel server and the static file server
CMD ["sh", "-c", "python squirrel_server.py & python3 -m http.server 8000"]
