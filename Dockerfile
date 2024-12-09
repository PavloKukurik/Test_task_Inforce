# Use the official Python image from the Docker Hub
FROM python:3.9-slim

RUN apt-get update && apt-get install -y postgresql-client

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the current directory into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

CMD ["./start.sh"]