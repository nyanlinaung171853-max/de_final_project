import logging


def validate_products(products):

    valid_products = []

    for product in products:

        product_id = product.get("id")
        title = product.get("title")
        price = product.get("price")
        stock = product.get("stock")

        if product_id is None:
            continue

        if not title:
            continue

        if price is None or price < 0:
            continue

        if stock is None or stock < 0:
            continue

        valid_products.append(product)

    logging.info(
        "Validation completed: %s valid products",
        len(valid_products)
    )

    return valid_products


def deduplicate_products(products):

    unique_products = {}

    for product in products:

        product_id = product.get("id")

        if product_id is not None:

            unique_products[product_id] = product

    return list(
        unique_products.values()
    )


def quality_check(products):

    if not products:
        raise ValueError(
            "Data Quality Failed: No data"
        )

    ids = []

    for product in products:

        product_id = product.get("id")

        if product_id is None:
            raise ValueError(
                "Product ID is missing"
            )

        ids.append(product_id)

        price = product.get("price")

        if price is None:
            raise ValueError(
                "Price is missing"
            )

        if price < 0:
            raise ValueError(
                "Invalid price"
            )

        stock = product.get("stock")

        if stock is None:
            raise ValueError(
                "Stock is missing"
            )

        if stock < 0:
            raise ValueError(
                "Invalid stock"
            )

        rating = product.get("rating")

        if rating is not None:

            if rating < 0 or rating > 5:
                raise ValueError(
                    "Invalid rating"
                )

    if len(ids) != len(set(ids)):
        raise ValueError(
            "Duplicate product IDs"
        )

    logging.info(
        "Data Quality Check: PASS"
    )

    return True