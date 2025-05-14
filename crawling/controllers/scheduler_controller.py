from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from services.location_crawler import crawl_foody_locations
from services.browsing_ids_crawler import crawl_browsing_ids
from services.browsing_infos_crawler import crawl_browsing_infos_with_list

# Thiết lập logger
logger = logging.getLogger(__name__)

# Khởi tạo scheduler
scheduler = BackgroundScheduler()

def scheduled_full_crawl():
    """
    Hàm thực hiện crawl đầy đủ được gọi bởi scheduler
    """
    try:
        logger.info("Starting scheduled full crawl...")
        
        # Crawl locations
        city_ids = crawl_foody_locations()
        logger.info(f"Found {len(city_ids)} cities.")

        all_requests = []

        # Crawl browsing IDs cho từng thành phố
        for city_id in city_ids:
            logger.info(f"Crawling browsing_ids for city_id = {city_id}...")
            try:
                browsing_requests = crawl_browsing_ids(city_id=city_id)
                all_requests.extend(browsing_requests)
            except Exception as e:
                logger.error(f"Failed to crawl city {city_id}: {str(e)}")
                continue

        logger.info(f"Total browsing requests to process: {len(all_requests)}")

        # Crawl thông tin chi tiết
        result = crawl_browsing_infos_with_list(all_requests)
        
        logger.info(f"Scheduled full crawl completed successfully: {result}")
        
    except Exception as e:
        logger.error(f"Error during scheduled full crawl: {str(e)}")

def start_scheduler():
    """
    Khởi động scheduler khi ứng dụng khởi chạy
    """
    # Cài đặt job chạy lúc 1 giờ sáng mỗi ngày (hoặc thời gian được cấu hình)
    scheduler.add_job(
        scheduled_full_crawl,
        CronTrigger(hour=1, minute=0),  # Thiết lập thời gian chạy định kỳ
        id="daily_full_crawl",
        name="Daily full crawl at 1 AM",
        replace_existing=True
    )
    
    # Bắt đầu scheduler
    scheduler.start()
    logger.info("Scheduler started - Full crawl scheduled to run daily at 1:00 AM")

def shutdown_scheduler():
    """
    Tắt scheduler khi ứng dụng kết thúc
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down") 