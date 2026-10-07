import psycopg2
from pathlib import Path

from pyspark.sql import SparkSession


BASE_DIR = Path(__file__).resolve().parent.parent

GOLD_PATH = (
    BASE_DIR
    / "data"
    / "gold"
    / "dim_product"
)


def load_products():

    spark = (
        SparkSession.builder
        .appName("GoldToPostgres")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel(
        "WARN"
    )

    df = spark.read.parquet(
        str(GOLD_PATH)
    )

    print(
        f"Loading {df.count()} products..."
    )

    connection = psycopg2.connect(
        host="postgres",
        port=5432,
        database="ecommerce",
        user="ecommerce",
        password="ecommerce"
    )

    cursor = connection.cursor()

    for row in df.collect():

        cursor.execute(
            """
            INSERT INTO dim_product (
                product_id,
                product_name,
                category,
                brand,
                sku,
                price,
                discount_percentage,
                discounted_price,
                rating,
                stock,
                stock_status
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            """,
            (
                row["id"],
                row["title"],
                row["category"],
                row["brand"],
                row["sku"],
                row["price"],
                row["discount_percentage"],
                row["discounted_price"],
                row["rating"],
                row["stock"],
                row["stock_status"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    spark.stop()

    print(
        "Gold data loaded into PostgreSQL."
    )


if __name__ == "__main__":
    load_products()