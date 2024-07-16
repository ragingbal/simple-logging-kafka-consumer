#!/bin/bash

# Check if the topic name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <topic-name>"
  exit 1
fi

TOPIC_NAME=$1

# Get the list of all consumer groups
CONSUMER_GROUPS=$(kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list)

# Iterate through each consumer group and check if it's active
for GROUP in $CONSUMER_GROUPS; do
  # Check the lag for the given consumer group and topic
  LAG_INFO=$(kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group $GROUP --topic $TOPIC_NAME)

  # Check if the consumer group has no active members
  if echo "$LAG_INFO" | grep -q "Consumer group .* has no active members"; then
    echo "Non-active consumer group: $GROUP"
  fi
done
