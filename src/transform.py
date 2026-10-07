import logging

def transform_products(products):
    transformed_products = []

    for product in products:
        price = float(
            product.get("price", 0)
        )
        discount = float(
            product.get("discountPercentage", 0)
        )
        stock = int(
            product.get("stock", 0)
        )
        discount_price = (
            price * (1 - discount / 100)
        )
        if stock == 0:
            stock_status = "Out of Stock"

        elif stock < 10:
            stock_status = "Low Stock"

        else:
            stock_status = "In Stock"

        transformed_product = {

            "id": product.get("id"),

            "title": product.get("title"),

            "category": product.get("category"),

            "price": price,

            "discount_percentage": discount,

            "discounted_price": round(
                discount_price,
                2
            ),

            "rating": product.get("rating"),

            "stock": stock,

            "stock_status": stock_status,

            "brand": product.get("brand"),

            "sku": product.get("sku")
        }

        transformed_products.append(
            transformed_product
        )

    logging.info(
        "Transformed %s products",
        len(transformed_products)
    )

    return transformed_products