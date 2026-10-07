"""
Spark Structured Streaming Consumer — Kafka → Silver (Parquet)

Features:
- Kafka topic ကနေ real-time ဖတ်
- JSON parse + schema validate
- Data quality checks
- Checkpointing (exactly-once)
- Partition/offset metadata သိမ်း
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_json, to_timestamp,
    current_timestamp, when, lit
)
from pyspark.sql.types import (
    StructType, StructField,
    IntegerType, StringType, DoubleType, TimestampType
)
import logging

# ==========================================
# Config
# ==========================================
KAFKA_BOOTSTRAP = "kafka:29092"
TOPIC = "products_stream"

SILVER_PATH = "/app/data/silver/products"
CHECKPOINT_PATH = "/app/checkpoints/products_stream"

# ==========================================
# Logging
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("spark-streaming")

# ==========================================
# Schema — API ရဲ့ products structure
# ==========================================
product_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("category", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("discountPercentage", DoubleType(), True),
    StructField("rating", DoubleType(), True),
    StructField("stock", IntegerType(), True),
    StructField("brand", StringType(), True),
    StructField("sku", StringType(), True),
    StructField("event_time", TimestampType(), True),
])

# ==========================================
# Spark Session
# ==========================================
def create_spark():
    return (
        SparkSession.builder
        .appName("ProductsKafkaStreaming")
        .config("spark.sql.shuffle.partitions", "3")
        .config("spark.streaming.stopGracefullyOnShutdown", "true")
        .getOrCreate()
    )

# ==========================================
# Read from Kafka
# ==========================================
def read_kafka(spark):
    return (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", TOPIC)
        .option("startingOffsets", "latest")
        .option("failOnDataLoss", "false")
        .option("maxOffsetsPerTrigger", 100)
        .load()
    )

# ==========================================
# Transform
# ==========================================
def transform(df):
    # Kafka metadata + parse JSON
    parsed = (
        df.select(
            col("partition").alias("kafka_partition"),
            col("offset").alias("kafka_offset"),
            col("timestamp").alias("kafka_timestamp"),
            from_json(
                col("value").cast("string"),
                product_schema
            ).alias("data")
        )
        .select(
            "kafka_partition",
            "kafka_offset",
            "kafka_timestamp",
            "data.*"
        )
    )

    # Data quality — null id ကို ဖယ်
    cleaned = parsed.filter(
        col("id").isNotNull() &
        col("title").isNotNull() &
        (col("price") > 0)
    )

    # Derived columns
    enriched = (
        cleaned
        .withColumn(
            "discounted_price",
            col("price") * (1 - col("discountPercentage") / 100)
        )
        .withColumn(
            "stock_status",
            when(col("stock") == 0, "out_of_stock")
            .when(col("stock") < 20, "low_stock")
            .otherwise("in_stock")
        )
        .withColumn("processed_at", current_timestamp())
        .withWatermark("event_time", "10 minutes")
        .withColumn("is_valid", ...)
        .withColumn("invalid_reason", ...)
    )

    return enriched

# ==========================================
# Write to Silver (Parquet)
# ==========================================
def write_silver(df):
    return (
        df.writeStream
        .format("parquet")
        .option("path", SILVER_PATH)
        .option("checkpointLocation", CHECKPOINT_PATH)
        .outputMode("append")
        .partitionBy("category")
        .trigger(processingTime="30 seconds")
        .start()
    )

# ==========================================
# Main
# ==========================================
def main():
    logger.info("Starting Spark Streaming...")
    logger.info("Kafka: %s", KAFKA_BOOTSTRAP)
    logger.info("Topic: %s", TOPIC)
    logger.info("Silver: %s", SILVER_PATH)

    spark = create_spark()
    spark.sparkContext.setLogLevel("WARN")

    kafka_df = read_kafka(spark)
    silver_df = transform(kafka_df)

    query = write_silver(silver_df)

    logger.info("Streaming started. Waiting for data...")

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("Stopping stream...")
        query.stop()
        spark.stop()
        logger.info("Stopped.")

if __name__ == "__main__":
    main()