from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType
from src.transform import transform_products
import pytest

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("test").getOrCreate()


def test_discounted_price(spark):
    schema = StructType([
        StructField("id", IntegerType()),
        StructField("price", DoubleType()),
        StructField("discount_percentage", DoubleType()),
    ])
    df = spark.createDataFrame([(1, 100.0, 10.0)], schema)

    result = transform_products(df).collect()
    assert result[0]["discounted_price"] == 90.0