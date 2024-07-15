import os
import logging
from kafka import KafkaConsumer, KafkaException

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get configurations from environment variables
KAFKA_BROKER_LIST = os.getenv('KAFKA_BROKER_LIST', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'default_topic')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'default_group')
KAFKA_AUTO_OFFSET_RESET = os.getenv('KAFKA_AUTO_OFFSET_RESET', 'earliest')  # 'earliest', 'latest', 'none'
KAFKA_CONSUMER_TIMEOUT_MS = int(os.getenv('KAFKA_CONSUMER_TIMEOUT_MS', '10000'))
KAFKA_SESSION_TIMEOUT_MS = int(os.getenv('KAFKA_SESSION_TIMEOUT_MS', '10000'))
KAFKA_HEARTBEAT_INTERVAL_MS = int(os.getenv('KAFKA_HEARTBEAT_INTERVAL_MS', '3000'))

def main():
    logger.info(f"Starting Kafka consumer for topic: {KAFKA_TOPIC}")

    try:
        # Create a Kafka consumer
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BROKER_LIST,
            group_id=KAFKA_GROUP_ID,
            auto_offset_reset=KAFKA_AUTO_OFFSET_RESET,
            enable_auto_commit=True,
            consumer_timeout_ms=KAFKA_CONSUMER_TIMEOUT_MS,
            session_timeout_ms=KAFKA_SESSION_TIMEOUT_MS,
            heartbeat_interval_ms=KAFKA_HEARTBEAT_INTERVAL_MS
        )

        logger.info("Kafka consumer started successfully. Waiting for messages...")

        # Consume messages from the Kafka topic
        for message in consumer:
            logger.info(f"Received message: {message.value.decode('utf-8')}")

    except KafkaException as e:
        logger.error(f"Kafka error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed.")

if __name__ == "__main__":
    main()
