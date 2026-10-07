import logging

from src.extract import extract_products
from src.transform import transform_products
from src.quality import (
    validate_products,
    deduplicate_products,
    quality_check
)
from src.load import (
    save_bronze,
    save_silver
)


logging.basicConfig(
    filename="logs/batch_pipeline.log",
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)


def run_batch():

    logging.info(
        "========== BATCH START =========="
    )

    try:

        # 1. Extract
        products = extract_products()

        # 2. Bronze
        bronze_file = save_bronze(
            products
        )

        logging.info(
            "Bronze saved: %s",
            bronze_file
        )

        # 3. Validate
        valid_products = validate_products(
            products
        )

        # 4. Deduplicate
        unique_products = (
            deduplicate_products(
                valid_products
            )
        )

        # 5. Transform
        transformed_products = (
            transform_products(
                unique_products
            )
        )

        # 6. Quality Check
        quality_check(
            transformed_products
        )

        # 7. Silver
        silver_file = save_silver(
            transformed_products
        )

        logging.info(
            "Silver saved: %s",
            silver_file
        )

        logging.info(
            "========== BATCH SUCCESS =========="
        )

        print(
            "Batch pipeline completed successfully."
        )

        print(
            f"Products processed: "
            f"{len(transformed_products)}"
        )

    except Exception as error:

        logging.exception(
            "Batch pipeline failed: %s",
            error
        )

        print(
            f"Batch pipeline failed: {error}"
        )


if __name__ == "__main__":
    run_batch()