from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import List
from services.location_crawler import crawl_foody_locations
from services.browsing_ids_crawler import crawl_browsing_ids
from services.browsing_infos_crawler import crawl_browsing_infos, crawl_browsing_infos_with_list
from schemas.browsing_info_schema import BrowsingInfosRequest
from utils.file_handler import save_to_json
import logging
import time

# Setup logger for this module
logger = logging.getLogger(__name__)

# Constants
MAX_DELIVERY_IDS_PER_CITY = 50  # Maximum number of delivery IDs to process per city

# Create router for crawling API
router = APIRouter(
    prefix="/api",
    tags=["crawling"],
)

@router.get("/crawl-locations")
def crawl_locations():
    """
    Crawl the list of cities from Foody
    """
    try:
        logger.info("Starting crawl locations API endpoint")
        file_saved = crawl_foody_locations()
        logger.info(f"Successfully saved locations to file")
        return {
            "status": "success", 
            "message": "Location data saved successfully",
            "data": {
                "file": file_saved
            }
        }
    except Exception as e:
        logger.error(f"Error crawling locations: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": f"Failed to crawl locations: {str(e)}",
                "data": None
            }
        )


@router.get("/crawl-browsing-ids")
def crawl_browsing(city_id: int = 218):
    """
    Crawl list of delivery IDs for a city
    """
    try:
        logger.info(f"Starting crawl browsing IDs for city_id: {city_id}")
        file_saved = crawl_browsing_ids(city_id)
        logger.info(f"Successfully saved browsing IDs for city_id: {city_id}")
        return {
            "status": "success",
            "message": f"Browsing IDs data saved for city {city_id}",
            "data": {
                "file": file_saved,
                "city_id": city_id
            }
        }
    except Exception as e:
        logger.error(f"Error crawling browsing IDs for city_id {city_id}: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": f"Failed to crawl browsing IDs: {str(e)}",
                "data": {
                    "city_id": city_id
                }
            }
        )


@router.get("/full-crawl")
def full_crawl():
    """
    Perform full crawl: locations -> browsing IDs -> browsing infos
    """
    try:
        logger.info("Starting full crawl process")
        city_ids, locations = crawl_foody_locations() 
        logger.info(f"Found {len(city_ids)} cities")

        all_requests = []

        for city_id in city_ids:
            logger.info(f"Crawling browsing IDs for city_id: {city_id}")
            try:
                browsing_requests = crawl_browsing_ids(city_id=city_id)
                
                # Limit the number of delivery_ids to process
                delivery_ids_to_process = browsing_requests["delivery_ids"][:MAX_DELIVERY_IDS_PER_CITY]
                logger.info(f"Processing {len(delivery_ids_to_process)} delivery IDs for city {city_id}")
                
                for delivery_id in delivery_ids_to_process:
                    all_requests.append(BrowsingInfosRequest(
                        delivery_ids=[delivery_id],
                        city_id=city_id
                    ))
                
                logger.debug(f"Added {len(delivery_ids_to_process)} requests for city: {city_id}")
            except Exception as e:
                logger.error(f"Failed to crawl city {city_id}: {e}", exc_info=True)
                continue

        logger.info(f"Total browsing requests to process: {len(all_requests)}")

        result = crawl_browsing_infos_with_list(all_requests)  
        try:
            # Lưu vào file JSON
            filename = f"foody_combined_data_{int(time.time())}.json"
            combined_data = {
                "locations": locations,
                "foods": result["all_foods"]
            }
            full_path = save_to_json(combined_data, filename)
            logger.info(f"Saved combined data to file: {full_path}")
        except Exception as e:
            logger.error(f"Error saving data to file: {str(e)}", exc_info=True)

        return {
            "status": "success",
            "message": "Full crawl completed successfully",
            "data": {
                "filename": filename,
                "total_cities": len(city_ids),
                "total_locations": len(locations),
                "total_foods": len(result["all_foods"])
            }
        }
    except Exception as e:
        logger.error(f"Error in full crawl: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": f"Failed to complete full crawl: {str(e)}",
                "data": None
            }
        )


@router.get("/crawl-by-city")
def crawl_by_city(city_id: int = Query(...)):
    """
    Crawl data for a specific city
    """
    try:
        logger.info(f"Starting crawl by city ID: {city_id}")
        delivery_infos = crawl_browsing_ids(city_id=city_id)
        
        browsing_infos_list = []
        
        # Limit the number of delivery_ids to process
        delivery_ids_to_process = delivery_infos["delivery_ids"][:MAX_DELIVERY_IDS_PER_CITY]
        logger.info(f"Processing {len(delivery_ids_to_process)} delivery IDs for city {city_id}")

        city_id = delivery_infos["city_id"]
        for delivery_id in delivery_ids_to_process:
            browsing_infos_list.append(BrowsingInfosRequest(
                delivery_ids=[delivery_id],
                city_id=city_id
            ))
        
        logger.info(f"Processing {len(browsing_infos_list)} requests for city: {city_id}")
        result = crawl_browsing_infos_with_list(browsing_infos_list)
        logger.info(f"Crawl by city {city_id} completed successfully")

        return {
            "status": "success",
            "message": f"Crawl by city {city_id} completed successfully",
            "data": {
                "filename": result["filename"],
                "city_id": city_id,
                "total_delivery_ids": len(delivery_infos["delivery_ids"]),
                "processed_delivery_ids": len(delivery_ids_to_process)
            }
        }
    except Exception as e:
        logger.error(f"Error crawling by city {city_id}: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": f"Failed to crawl city {city_id}: {str(e)}",
                "data": {
                    "city_id": city_id
                }
            }
        ) 