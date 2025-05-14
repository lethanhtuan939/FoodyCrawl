# utils/file_handler.py
import os
import json

LANDING_ZONE_PATH = "landing_zone"

def save_to_json(data, filename):
    os.makedirs(LANDING_ZONE_PATH, exist_ok=True)
    full_path = os.path.join(LANDING_ZONE_PATH, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return full_path
