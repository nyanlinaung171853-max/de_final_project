import logging
import requests

from src.config import API_URL, REQUEST_TIMEOUT

def extract_products():
    limit = 30
    skip = 0
    max_retries = 3
    all_products = []

    while True:
        params = {
            "limit": limit,
            "skip": skip
        }
        for attempt in range(1, max_retries+1):
            try:
                logging.info(
                    "Requesting API: skip=%s limit=%s attempt=%s",
                    skip,
                    limit,
                    attempt
                )
                response = requests.get(
                    API_URL,
                    params=params,
                    timeout=REQUEST_TIMEOUT
                )
                response.raise_for_status()
                data = response.json()
                products = data.get("products", [])

                total = data.get("total", 0)

                all_products.extend(products)

                logging.info(
                    "Received %s products. "
                    "Collected %s/%s",
                    len(products),
                    len(all_products),
                    total
                )

                break
            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError
            ) as error:
                logging.warning(
                    "Attempt %s failed: %s",
                    attempt,
                    error
                )
                if attempt == max_retries:
                    raise

        if len(all_products) >= total:
            break
        if not products:
            break

        skip += limit

    logging.info("Extraction complete: %s products",
                 len(all_products))
    return all_products
