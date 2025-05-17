# services/browsing_ids_crawler.py
import requests
import logging
import random
import time

# Create logger for this module
logger = logging.getLogger(__name__)

def crawl_browsing_ids(city_id=218, root_category=1000000) -> dict:
    """
    Call API to get list of delivery_ids by city_id.
    Returns a dict containing delivery_ids and city_id.
    """
    logger.info(f"Crawling browsing IDs for city_id: {city_id}, root_category: {root_category}")
    url = "https://gappapi.deliverynow.vn/api/delivery/get_browsing_ids"

    headers = {
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "x-foody-api-version": "1",
        "x-foody-app-type": "1004",
        "x-foody-client-id": "",
        "x-foody-client-type": "1",
        "x-foody-client-version": "1",
        "Content-Type": "application/json"
    }

    payload = {
        "sort_type": 2,
        "city_id": city_id,
        "root_category": root_category,
        "root_category_ids": [root_category]
    }

    try:
        logger.debug(f"Sending request to {url} with payload.city_id: {payload['city_id']}")
        
        # Sleep randomly between 0.5 and 1.0 seconds before making the request
        time_to_sleep = random.uniform(0.5, 1.0)
        logger.debug(f"Sleeping for {time_to_sleep:.2f} seconds before request...")
        time.sleep(time_to_sleep)
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug("Successfully received response from browsing_ids API")

        delivery_ids = data.get("reply", {}).get("delivery_ids", [])
        logger.info(f"Found {len(delivery_ids)} delivery IDs for city {city_id}")
        
        return {
            "city_id": city_id,
            "delivery_ids": delivery_ids
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling browsing_ids API: {str(e)}", exc_info=True)
        return {
            "city_id": city_id,
            "delivery_ids": [],
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in crawl_browsing_ids: {str(e)}", exc_info=True)
        return {
            "city_id": city_id,
            "delivery_ids": [],
            "error": str(e)
        }
    # return delivery_ids
