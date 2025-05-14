# services/location_crawler.py
import requests
import time
from utils.file_handler import save_to_json
from schemas.location_schema import Location

def crawl_foody_locations() -> list[int]:
    url = "https://www.foody.vn/__get/Common/GetPopupLocation"

    headers = {
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Content-type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/136.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Lấy danh sách location
    raw_locations = data.get("AllLocations", [])

    # Chuyển về dạng schema Location
    locations = [
        Location(
            city_id=loc["Id"],
            country_id=loc["CountryId"],
            name=loc["Name"],
            country_name=loc["CountryName"]
        ).dict()
        for loc in raw_locations
    ]

    # Lưu vào file JSON
    filename = f"foody_locations_{int(time.time())}.json"
    save_to_json(locations, filename)

    # Trả về danh sách city_id
    city_ids = [loc["city_id"] for loc in locations]
    return city_ids
