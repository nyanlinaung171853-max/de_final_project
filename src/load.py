import json
import csv

from src.config import (
    BRONZE_DIR,
    SILVER_DIR
)


def save_bronze(products):

    output_dir = BRONZE_DIR / "products"

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir / "products.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            products,
            file,
            ensure_ascii=False,
            indent=2
        )

    return output_file


def save_silver(products):

    if not products:
        raise ValueError(
            "No products to save"
        )

    output_dir = (
        SILVER_DIR / "products"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir / "products.csv"
    )

    fieldnames = products[0].keys()

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(products)

    return output_file