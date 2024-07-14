# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables for Kafka configuration with default values
ENV KAFKA_BROKER_LIST=localhost:9092
ENV KAFKA_TOPIC=default_topic
ENV KAFKA_GROUP_ID=default_group
ENV KAFKA_AUTO_OFFSET_RESET=earliest
ENV KAFKA_CONSUMER_TIMEOUT_MS=10000
ENV KAFKA_SESSION_TIMEOUT_MS=10000
ENV KAFKA_HEARTBEAT_INTERVAL_MS=3000

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Kafka consumer script into the container
COPY app.py .

# Run the Kafka consumer script
CMD ["python", "app.py"]