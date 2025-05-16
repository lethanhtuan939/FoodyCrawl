import logging
import os
from logging.handlers import RotatingFileHandler
import time

def setup_logging(log_level=logging.INFO):
    """
    Setup logging configuration for the entire application
    Including:
    - Console logging
    - File logging with rotation
    - Format logs with timestamp, level, module and message
    """
    # Get crawling directory - only go up one level from utils
    crawling_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create logs directory inside crawling directory
    log_dir = os.path.join(crawling_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log filename with timestamp
    log_filename = os.path.join(log_dir, f"crawling_{time.strftime('%Y%m%d')}.log")
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear old handlers (if any) to avoid duplicate logs
    if root_logger.handlers:
        root_logger.handlers.clear()
    
    # Handler for console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Handler for file with rotation (max 5MB per file, keep 10 files)
    file_handler = RotatingFileHandler(
        log_filename, 
        maxBytes=5*1024*1024,  # 5MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    root_logger.addHandler(file_handler)
    
    # Set level for third-party modules
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    # Log when started
    logging.info(f"Logging has been setup, writing logs to: {log_filename}")
    
    return root_logger 