# utils/file_handler.py
import os
import json
import logging

# Setup logger for this module
logger = logging.getLogger(__name__)

# In Docker, the landing_zone will be at /app/landing_zone (from the volume mount)
# In development, it will be at [project_root]/landing_zone

# Check if we're running in Docker
if os.path.exists('/app/landing_zone'):
    LANDING_ZONE_PATH = '/app/landing_zone'
    logger.info(f"Running in Docker, landing zone path: {LANDING_ZONE_PATH}")
else:
    # Get the project root directory (2 levels up from this file)
    CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    LANDING_ZONE_PATH = os.path.join(CURRENT_DIR, "landing_zone")
    logger.info(f"Running in development, landing zone path: {LANDING_ZONE_PATH}")

def save_to_json(data, filename):
    os.makedirs(LANDING_ZONE_PATH, exist_ok=True)
    full_path = os.path.join(LANDING_ZONE_PATH, filename)
    logger.info(f"Saving data to file: {full_path}")
    
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"File saved successfully at: {full_path}")
    return full_path
