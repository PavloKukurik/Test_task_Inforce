# Use the official Python image based on Alpine to reduce the container size
FROM python:3.9-alpine

# Update apk package index and install PostgreSQL client
RUN apk update && apk add postgresql-client

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements.txt file first to optimize Docker cache usage
COPY requirements.txt /app/

# Install Python dependencies listed in requirements.txt (no-cache to keep the image smaller)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Copy the bash script and make it executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Start the container by executing the bash script
CMD ["./run.bash"]
