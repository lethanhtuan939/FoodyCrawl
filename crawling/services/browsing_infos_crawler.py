# services/browsing_infos_crawler.py

import requests
import time
from typing import Union, List
from schemas.browsing_info_schema import BrowsingInfosRequest
from schemas.food_schema import Food
from utils.file_handler import save_to_json
import random
import logging

# Create logger for this module
logger = logging.getLogger(__name__)

# Trả về List[Food] chứ không phải filename
def crawl_browsing_infos(request_data: Union[dict, BrowsingInfosRequest]) -> List[Food]:
    """
    Crawl restaurant information based on the provided request data
    Returns a list of Food objects
    """
    if isinstance(request_data, dict):
        request_model = BrowsingInfosRequest(**request_data)
    elif isinstance(request_data, BrowsingInfosRequest):
        request_model = request_data
    else:
        logger.error(f"Invalid request data type: {type(request_data)}")
        raise ValueError("Invalid request data")

    url = "https://gappapi.deliverynow.vn/api/delivery/get_browsing_infos"
    headers = {
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Content-Type": "application/json",
        "x-foody-api-version": "1",
        "x-foody-app-type": "1004",
        "x-foody-client-type": "1",
        "x-foody-client-id": "",
        "x-foody-client-version": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }

    food_list: List[Food] = []
    try:
        logger.debug(f"Sending request to browsing_infos API for delivery_id: {request_model.delivery_ids}")
        response = requests.post(url, headers=headers, json=request_model.dict())
        response.raise_for_status()
        data = response.json()
        logger.debug("Successfully received response from browsing_infos API")

        delivery_infos = data.get("reply", {}).get("delivery_infos", [])
        logger.info(f"Found {len(delivery_infos)} restaurant items in response")

        for item in delivery_infos:
            photos = item.get("photos", [])
            image_url = ""

            # Chỉ lấy ảnh có width = 240 và height = 240
            for photo in photos:
                if photo.get("width") == 240 and photo.get("height") == 240:
                    image_url = photo.get("value", "")
                    break  # Dừng vòng lặp ngay khi tìm thấy ảnh phù hợp
            food = Food(
                name=item.get("name", ""),
                categories=", ".join(item.get("categories", [])),
                cuisines=", ".join(item.get("cuisines", [])),
                address=item.get("address", ""),
                rating_avg=item.get("rating", {}).get("avg"),
                rating_total_review=item.get("rating", {}).get("total_review"),
                image_url=image_url,
                is_open=item.get("is_open", True),
                city_id=item.get("city_id", 0)
            )
            food_list.append(food)
        
        logger.debug(f"Successfully processed {len(food_list)} food items")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling browsing_infos API: {str(e)}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error in crawl_browsing_infos: {str(e)}", exc_info=True)

    return food_list


def crawl_browsing_infos_with_list(requests_list: List[BrowsingInfosRequest]):
    """
    Process a list of browsing requests and return the results
    """
    logger.info(f"Starting to process {len(requests_list)} browsing requests")
    all_foods = []

    for i, req in enumerate(requests_list):
        try:
            logger.debug(f"Processing request {i+1}/{len(requests_list)}: {req}")
            food_items = crawl_browsing_infos(req)  # giờ trả về list of Food
            all_foods.extend([f.dict() for f in food_items])  # convert Food -> dict
            logger.debug(f"Added {len(food_items)} food items, total items so far: {len(all_foods)}")

            # ⬇️ Sleep ngẫu nhiên để tránh bị block
            time_to_sleep = random.uniform(0.5, 1.0)
            logger.debug(f"Sleeping for {time_to_sleep:.2f} seconds...")
            time.sleep(time_to_sleep)
        except Exception as e:
            logger.error(f"Error processing request {req}: {str(e)}", exc_info=True)
            continue

    return {
        "result": "success",
        "all_foods": all_foods,
        "total_restaurants": len(all_foods)
    }
