# services/browsing_ids_crawler.py
import requests

def crawl_browsing_ids(city_id=218, root_category=1000000) -> dict:
    """
    Gọi API lấy danh sách delivery_ids theo city_id.
    Trả về một dict gồm delivery_ids và city_id.
    """

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

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    delivery_ids = data.get("reply", {}).get("delivery_ids", [])
    
    return {
        "city_id": city_id,
        "delivery_ids": delivery_ids
    }
    # return delivery_ids
