from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    count,
    sum,
    round
)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SILVER_FILE = (
    BASE_DIR
    / "data"
    / "silver"
    / "products"
    / "products.csv"
)

GOLD_DIR = (
    BASE_DIR
    / "data"
    / "gold"
)


def main():

    spark = (
        SparkSession.builder
        .appName("ECommerceGoldPipeline")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    print("Reading Silver data...")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(SILVER_FILE))
    )

    print("Silver schema:")
    df.printSchema()

    print("Silver data:")

    df.show(10, truncate=False)

    # ==========================================
    # Gold Dimension
    # ==========================================

    dim_product = df.select(
        "id",
        "title",
        "category",
        "brand",
        "sku",
        "price",
        "discount_percentage",
        "discounted_price",
        "rating",
        "stock",
        "stock_status"
    )

    dim_product = dim_product.dropDuplicates(
        ["id"]
    )

    # ==========================================
    # Gold Analytics
    # ==========================================

    category_summary = (
        df.groupBy("category")
        .agg(
            count("*").alias(
                "product_count"
            ),

            round(
                avg("price"),
                2
            ).alias(
                "average_price"
            ),

            sum("stock").alias(
                "total_stock"
            ),

            round(
                avg("rating"),
                2
            ).alias(
                "average_rating"
            )
        )
        .orderBy(
            "product_count",
            ascending=False
        )
    )

    # ==========================================
    # Save Gold
    # ==========================================

    dim_product_path = (
        GOLD_DIR / "dim_product"
    )

    category_summary_path = (
        GOLD_DIR
        / "product_category_summary"
    )

    (
        dim_product
        .write
        .mode("overwrite")
        .parquet(
            str(dim_product_path)
        )
    )

    (
        category_summary
        .write
        .mode("overwrite")
        .parquet(
            str(category_summary_path)
        )
    )

    print()
    print("Gold dim_product:")

    dim_product.show(
        10,
        truncate=False
    )

    print()
    print("Gold category summary:")

    category_summary.show(
        truncate=False
    )

    spark.stop()

    print()
    print(
        "PySpark Gold pipeline completed successfully."
    )


if __name__ == "__main__":
    main()