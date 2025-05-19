from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from services.location_crawler import crawl_foody_locations
from services.browsing_ids_crawler import crawl_browsing_ids
from services.browsing_infos_crawler import crawl_browsing_infos, crawl_browsing_infos_with_list
from schemas.browsing_info_schema import BrowsingInfosRequest
from utils.file_handler import save_to_json
import time

# Setup logger for this module
logger = logging.getLogger(__name__)

# Initialize scheduler
scheduler = BackgroundScheduler()

# Constants
MAX_DELIVERY_IDS_PER_CITY = 50  # Maximum number of delivery IDs to process per city

def scheduled_full_crawl():
    """
    Function to perform full crawl called by scheduler
    """
    try:
        logger.info("Starting scheduled full crawl...")
        
        # Crawl locations
        city_ids, locations = crawl_foody_locations()
        logger.info(f"Found {len(city_ids)} cities")

        all_requests = []

        # Crawl browsing IDs for each city
        for city_id in city_ids:
            logger.info(f"Crawling browsing IDs for city_id: {city_id}")
            try:
                browsing_result = crawl_browsing_ids(city_id=city_id)
                if "error" not in browsing_result:
                    # Limit the number of delivery_ids to process
                    delivery_ids_to_process = browsing_result["delivery_ids"][:MAX_DELIVERY_IDS_PER_CITY]
                    logger.info(f"Processing {len(delivery_ids_to_process)} delivery IDs for city {city_id}")
                    
                    for delivery_id in delivery_ids_to_process:
                        all_requests.append(BrowsingInfosRequest(
                            delivery_ids=[delivery_id],
                            city_id=city_id
                        ))
                else:
                    logger.error(f"Error in browsing_ids result: {browsing_result.get('error')}")
            except Exception as e:
                logger.error(f"Failed to crawl city {city_id}: {str(e)}", exc_info=True)
                continue

        logger.info(f"Total browsing requests to process: {len(all_requests)}")

        # Crawl detailed information
        if all_requests:
            result = crawl_browsing_infos_with_list(all_requests)
            
            # Save combined data to a single file
            try:
                filename = f"foody_combined_data_{int(time.time())}.json"
                combined_data = {
                    "locations": locations,
                    "foods": result["all_foods"]
                }
                full_path = save_to_json(combined_data, filename)
                logger.info(f"Saved combined data to file: {full_path}")
            except Exception as e:
                logger.error(f"Error saving data to file: {str(e)}", exc_info=True)
            
            logger.info(f"Scheduled full crawl completed successfully: {result.get('total_restaurants', 0)} restaurants found")
        else:
            logger.warning("No requests to process, skipping crawl_browsing_infos")
        
    except Exception as e:
        logger.error(f"Error during scheduled full crawl: {str(e)}", exc_info=True)

def start_scheduler():
    """
    Start scheduler when application starts
    """
    # Configure job to run at 1 AM every day (or configured time)
    scheduler.add_job(
        scheduled_full_crawl,
        CronTrigger(hour=1, minute=0),  # Set scheduled time
        id="daily_full_crawl",
        name="Daily full crawl at 1 AM",
        replace_existing=True
    )
    
    # Start scheduler
    scheduler.start()
    logger.info("Scheduler started - Full crawl scheduled to run daily at 1:00 AM")

def shutdown_scheduler():
    """
    Shut down scheduler when application terminates
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down") 