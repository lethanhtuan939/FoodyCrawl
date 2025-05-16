# services/location_crawler.py
import requests
import time
import logging
import os
import random
from utils.file_handler import save_to_json
from schemas.location_schema import Location

# Tạo logger cho module này
logger = logging.getLogger(__name__)

def crawl_foody_locations() -> list[int]:
    """
    Crawl danh sách các địa điểm từ Foody.vn
    Trả về danh sách các city_id
    """
    logger.info("Starting crawl for Foody locations")
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

    try:
        # Sleep randomly between 0.5 and 1.0 seconds before making the request
        time_to_sleep = random.uniform(0.5, 1.0)
        logger.debug(f"Sleeping for {time_to_sleep:.2f} seconds before request...")
        time.sleep(time_to_sleep)
        
        logger.debug(f"Sending request to {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.debug("Successfully received response from locations API")

        # Lấy danh sách location
        raw_locations = data.get("AllLocations", [])
        logger.info(f"Found {len(raw_locations)} locations")

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
        logger.debug(f"Converted {len(locations)} locations to schema format")

        try:
            # Lưu vào file JSON
            filename = f"foody_locations_{int(time.time())}.json"
            full_path = save_to_json(locations, filename)
            logger.info(f"Saved locations list to file: {full_path}")
        except Exception as e:
            logger.error(f"Error saving locations to file: {str(e)}", exc_info=True)

        # Trả về danh sách city_id
        city_ids = [loc["city_id"] for loc in locations]
        logger.info(f"Returning {len(city_ids)} city IDs")
        
        return city_ids
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling locations API: {str(e)}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Unexpected error in crawl_foody_locations: {str(e)}", exc_info=True)
        return []
