"""
Kafka Producer — Products API → Kafka topic

Features:
- API ကနေ data ဆွဲ
- Key (product_id) ထည့် → same product → same partition
- Error handling + retry
- Graceful shutdown (Ctrl+C)
- Rate limiting
"""

import json
import time
import signal
import sys
import logging
import requests

from kafka import KafkaProducer
from kafka.errors import KafkaError

# ==========================================
# Config
# ==========================================
KAFKA_BOOTSTRAP = "kafka:29092"
TOPIC = "products_stream"
API_URL = "https://dummyjson.com/products"

POLL_INTERVAL = 10       # စက္ကန့်
PAGE_SIZE = 10           # တစ်ခါ API ကနေ ဆွဲတဲ့ အရေအတွက်
MAX_RETRIES = 3

# ==========================================
# Logging
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("kafka-producer")

# ==========================================
# Graceful shutdown
# ==========================================
running = True

def shutdown(signum, frame):
    global running
    logger.info("Shutdown signal received. Stopping...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# ==========================================
# Kafka Producer
# ==========================================
def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        key_serializer=lambda k: str(k).encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",              # all replicas confirm
        retries=5,
        linger_ms=10,            # batch အတွက် ခဏစောင့်
        compression_type="gzip"  # network သေးအောင်
    )

# ==========================================
# Fetch API with retry
# ==========================================
def fetch_products(skip=0, limit=PAGE_SIZE):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                API_URL,
                params={"limit": limit, "skip": skip},
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("products", [])
        except requests.exceptions.RequestException as e:
            logger.warning("API attempt %s failed: %s", attempt, e)
            if attempt == MAX_RETRIES:
                logger.error("API failed after %s attempts", MAX_RETRIES)
                return []
            time.sleep(2)

    return []

# ==========================================
# Send with delivery confirmation
# ==========================================
def on_send_success(record_metadata):
    logger.info(
        "✓ topic=%s partition=%s offset=%s",
        record_metadata.topic,
        record_metadata.partition,
        record_metadata.offset
    )

def on_send_error(exc):
    logger.error("✗ send failed: %s", exc)

def send_product(producer, product):
    """
    Key = product_id → same product → same partition
    (ordering ထိန်းဖို့)
    """
    producer.send(
        TOPIC,
        key=str(product["id"]),
        value=product
    ).add_callback(on_send_success).add_errback(on_send_error)

# ==========================================
# Main loop
# ==========================================
def main():
    logger.info("Connecting to Kafka at %s", KAFKA_BOOTSTRAP)

    try:
        producer = create_producer()
    except KafkaError as e:
        logger.error("Could not connect to Kafka: %s", e)
        sys.exit(1)

    logger.info("Producer connected. Topic: %s", TOPIC)

    skip = 0
    total_sent = 0

    while running:
        products = fetch_products(skip=skip, limit=PAGE_SIZE)

        if not products:
            logger.warning("No products fetched. Retry in %ss", POLL_INTERVAL)
            time.sleep(POLL_INTERVAL)
            continue

        for product in products:
            if not running:
                break
            send_product(producer, product)
            total_sent += 1

        producer.flush()
        logger.info(
            "Batch sent: %s products. Total: %s",
            len(products), total_sent
        )

        # Pagination — နောက်ဆုံးရောက်ရင် ပြန်စ
        skip += PAGE_SIZE
        if skip >= 100:
            skip = 0

        time.sleep(POLL_INTERVAL)

    logger.info("Flushing and closing producer...")
    producer.flush()
    producer.close()
    logger.info("Producer stopped. Total sent: %s", total_sent)

if __name__ == "__main__":
    main()