from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import List
from services.location_crawler import crawl_foody_locations
from services.browsing_ids_crawler import crawl_browsing_ids
from services.browsing_infos_crawler import crawl_browsing_infos, crawl_browsing_infos_with_list
from schemas.browsing_info_schema import BrowsingInfosRequest
import logging

# Thiết lập logger
logger = logging.getLogger(__name__)

# Tạo router cho crawling API
router = APIRouter(
    prefix="/api",
    tags=["crawling"],
)

@router.get("/crawl-locations")
def crawl_locations():
    """
    Crawl danh sách các thành phố từ Foody
    """
    try:
        file_saved = crawl_foody_locations()
        return {
            "status": "success", 
            "message": "Location data saved successfully",
            "data": {
                "file": file_saved
            }
        }
    except Exception as e:
        logger.error(f"Error crawling locations: {str(e)}")
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
    Crawl danh sách delivery IDs cho một thành phố
    """
    try:
        file_saved = crawl_browsing_ids(city_id)
        return {
            "status": "success",
            "message": f"Browsing IDs data saved for city {city_id}",
            "data": {
                "file": file_saved,
                "city_id": city_id
            }
        }
    except Exception as e:
        logger.error(f"Error crawling browsing IDs: {str(e)}")
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
    Thực hiện crawl đầy đủ: locations -> browsing IDs -> browsing infos
    """
    try:
        city_ids = crawl_foody_locations() 
        logger.info(f"Found {len(city_ids)} cities.")

        all_requests = []

        for city_id in city_ids:
            logger.info(f"Crawling browsing_ids for city_id = {city_id}...")
            try:
                browsing_requests = crawl_browsing_ids(city_id=city_id)  
                all_requests.extend(browsing_requests)  
            except Exception as e:
                logger.error(f"Failed to crawl city {city_id}: {e}")
                continue

        logger.info(f"Total browsing requests to process: {len(all_requests)}")

        result = crawl_browsing_infos_with_list(all_requests)  

        return {
            "status": "success",
            "message": "Full crawl completed successfully",
            "data": {
                "filename": result["filename"],
                "total_cities": len(city_ids),
                "total_requests": len(all_requests)
            }
        }
    except Exception as e:
        logger.error(f"Error in full crawl: {str(e)}")
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
    Crawl dữ liệu cho một thành phố cụ thể
    """
    try:
        delivery_infos = crawl_browsing_ids(city_id=city_id)
        
        browsing_infos_list = []

        city_id = delivery_infos["city_id"]
        for delivery_id in delivery_infos["delivery_ids"]:
            browsing_infos_list.append(BrowsingInfosRequest(
                delivery_ids=[delivery_id],
                city_id=city_id
            ))
        result = crawl_browsing_infos_with_list(browsing_infos_list)

        return {
            "status": "success",
            "message": f"Crawl by city {city_id} completed successfully",
            "data": {
                "filename": result["filename"],
                "city_id": city_id,
                "total_delivery_ids": len(delivery_infos["delivery_ids"])
            }
        }
    except Exception as e:
        logger.error(f"Error crawling by city: {str(e)}")
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