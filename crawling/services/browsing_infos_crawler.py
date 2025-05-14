# services/browsing_infos_crawler.py

import requests
import time
from typing import Union, List
from schemas.browsing_info_schema import BrowsingInfosRequest
from schemas.food_schema import Food
from utils.file_handler import save_to_json
import random

# Trả về List[Food] chứ không phải filename
def crawl_browsing_infos(request_data: Union[dict, BrowsingInfosRequest]) -> List[Food]:
    if isinstance(request_data, dict):
        request_model = BrowsingInfosRequest(**request_data)
    elif isinstance(request_data, BrowsingInfosRequest):
        request_model = request_data
    else:
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

    response = requests.post(url, headers=headers, json=request_model.dict())
    response.raise_for_status()
    data = response.json()

    delivery_infos = data.get("reply", {}).get("delivery_infos", [])

    food_list: List[Food] = []
    for item in delivery_infos:
        food = Food(
            name=item.get("name", ""),
            categories=", ".join(item.get("categories", [])),
            cuisines=", ".join(item.get("cuisines", [])),
            address=item.get("address", ""),
            rating_avg=item.get("rating", {}).get("avg"),
            rating_total_review=item.get("rating", {}).get("total_review"),
            is_open=item.get("is_open", True),
            city_id=item.get("city_id", 0)
        )
        food_list.append(food)

    return food_list


def crawl_browsing_infos_with_list(requests_list: List[BrowsingInfosRequest]):
    all_foods = []

    for req in requests_list:
        print(f"request: {req}")
        food_items = crawl_browsing_infos(req)  # giờ trả về list of Food
        all_foods.extend([f.dict() for f in food_items])  # convert Food -> dict để ghi file

        # ⬇️ Sleep ngẫu nhiên để tránh bị block
        time_to_sleep = random.uniform(1.5, 3.0)
        print(f"Sleeping for {time_to_sleep:.2f} seconds...")
        time.sleep(time_to_sleep)

    filename = f"foody_foods_{int(time.time())}.json"
    save_to_json(all_foods, filename)

    return {
        "result": "success",
        "total_restaurants": len(all_foods),
        "filename": filename
    }
