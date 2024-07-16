# List non-active consumers

Here's a shell script that lists all non-active consumer groups for a specific Kafka topic. This script assumes you have `kafka-consumer-groups.sh` available in your `PATH`.

```bash
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
```

### How to Use the Script
1. Save the script to a file, for example, `list_non_active_consumer_groups.sh`.
2. Make the script executable:
   ```bash
   chmod +x list_non_active_consumer_groups.sh
   ```
3. Run the script with the Kafka topic name as an argument:
   ```bash
   ./list_non_active_consumer_groups.sh <topic-name>
   ```

Replace `<topic-name>` with the name of your Kafka topic.

### Assumptions
- Kafka is running on `localhost:9092`.
- `kafka-consumer-groups.sh` is available in your `PATH`. If it's not, you might need to provide the full path to `kafka-consumer-groups.sh` in the script.
- The script checks for consumer groups with no active members for the specified topic. Adjust the script if your setup or requirements are different.




# Delete non-active cosumers USE WITH CARE


Certainly! Here's a shell script that takes a Kafka topic name, lists all consumer groups consuming from that topic, and then deletes those consumer groups. This script assumes you have `kafka-consumer-groups.sh` available in your `PATH`.

```bash
#!/bin/bash

# Check if the topic name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <topic-name>"
  exit 1
fi

TOPIC_NAME=$1

# Get the list of all consumer groups
CONSUMER_GROUPS=$(kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list)

# Iterate through each consumer group and check if it's consuming from the given topic
for GROUP in $CONSUMER_GROUPS; do
  # Check the lag for the given consumer group and topic
  LAG_INFO=$(kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group $GROUP --topic $TOPIC_NAME 2>&1)
  
  # Check if the consumer group is consuming from the given topic
  if echo "$LAG_INFO" | grep -q "$TOPIC_NAME"; then
    echo "Deleting consumer group: $GROUP consuming from topic: $TOPIC_NAME"
    kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group $GROUP
  fi
done
```

### How to Use the Script
1. Save the script to a file, for example, `delete_consumer_groups.sh`.
2. Make the script executable:
   ```bash
   chmod +x delete_consumer_groups.sh
   ```
3. Run the script with the Kafka topic name as an argument:
   ```bash
   ./delete_consumer_groups.sh <topic-name>
   ```

Replace `<topic-name>` with the name of your Kafka topic.

### Assumptions
- Kafka is running on `localhost:9092`.
- `kafka-consumer-groups.sh` is available in your `PATH`. If it's not, you might need to provide the full path to `kafka-consumer-groups.sh` in the script.
- The script deletes consumer groups that are consuming from the specified topic. Adjust the script if your setup or requirements are different.