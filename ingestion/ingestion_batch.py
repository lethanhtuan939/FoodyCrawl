import json
import os
import uuid
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from pydantic import ValidationError

from database import engine, SessionLocal, LocationDB, FoodDB, init_db
from models import Food, Location

LANDING_ZONE = "/app/landing_zone"

def ingest_json_data(file_path):
    time.sleep(1)  # Wait for file completion
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        locations = data.get("locations", [])
        foods = data.get("foods", [])
        print(f"New JSON file detected: {os.path.basename(file_path)} with {len(locations)} locations and {len(foods)} foods")
        print(f"Sample location data: {json.dumps(locations[:2], indent=2)}")
        print(f"Sample food data: {json.dumps(foods[:2], indent=2)}")

        db = SessionLocal()
        try:
            for location_data in locations:
                try:
                    location_data = {
                        "id": location_data.get("id", int(uuid.uuid4().int & (1<<31)-1)) if location_data.get("id") is None else location_data.get("id"),
                        "city_id": location_data.get("city_id", 0),
                        "country_id": location_data.get("country_id", 0),
                        "name": location_data.get("name", ""),
                        "country_name": location_data.get("country_name", "")
                    }
                    location = Location(**location_data)
                    location_db = LocationDB(
                        id=location.id,
                        city_id=location.city_id,
                        country_id=location.country_id,
                        name=location.name,
                        country_name=location.country_name
                    )
                    db.merge(location_db)
                    db.commit()
                    print(f"Inserted/Updated location with city_id: {location.city_id}")
                except ValidationError as ve:
                    print(f"Validation error for location in {file_path}: {str(ve)}")
                    print(f"Problematic location data: {json.dumps(location_data, indent=2)}")
                    db.rollback()
                    continue
                except Exception as e:
                    print(f"Error processing location in {file_path}: {str(e)}")
                    db.rollback()
                    continue

            for index, food_data in enumerate(foods):
                try:
                    if "id" not in food_data or food_data["id"] is None:
                        food_data["id"] = int(uuid.uuid4().int & (1<<31)-1)

                    if isinstance(food_data.get("categories"), str):
                        food_data["categories"] = [food_data["categories"]] if food_data["categories"] else []
                    elif not isinstance(food_data.get("categories"), list):
                        food_data["categories"] = []
                    
                    if isinstance(food_data.get("cuisines"), str):
                        food_data["cuisines"] = [food_data["cuisines"]] if food_data["cuisines"] else []
                    elif not isinstance(food_data.get("cuisines"), list):
                        food_data["cuisines"] = []

                    food_data["name"] = food_data.get("name", "")
                    food_data["address"] = food_data.get("address", "")
                    food_data["image_url"] = food_data.get("image_url", "")
                    food_data["rating_avg"] = float(food_data.get("rating_avg", 0.0))
                    food_data["rating_total_review"] = int(food_data.get("rating_total_review", 0))
                    food_data["is_open"] = bool(food_data.get("is_open", False))
                    food_data["city_id"] = int(food_data.get("city_id", 0))

                    food = Food(**food_data)

                    existing_location = db.query(LocationDB).filter(LocationDB.city_id == food.city_id).first()
                    if not existing_location:
                        print(f"City ID {food.city_id} not found in locations table, skipping food item: {food.name}")
                        continue

                    food_db = FoodDB(
                        id=food.id,
                        name=food.name,
                        categories=food.categories,
                        cuisines=food.cuisines,
                        address=food.address,
                        image_url=food.image_url,
                        rating_avg=food.rating_avg,
                        rating_total_review=food.rating_total_review,
                        is_open=food.is_open,
                        city_id=food.city_id
                    )
                    db.merge(food_db)
                    db.commit()
                    print(f"Inserted/Updated food with id: {food.id}")

                except ValidationError as ve:
                    print(f"Validation error for food in {file_path}: {str(ve)}")
                    print(f"Problematic food data: {json.dumps(food_data, indent=2)}")
                    db.rollback()
                    continue
                except Exception as e:
                    print(f"Error processing food in {file_path}: {str(e)}")
                    db.rollback()
                    continue

            print(f"Successfully ingested data from {file_path} into database at {datetime.now()}")
        finally:
            db.close()

    except Exception as e:
        print(f"Error reading JSON file {file_path}: {str(e)}")

class JSONFileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Event detected: type={event.event_type}, path={event.src_path}, is_directory={event.is_directory}")
        if event.src_path.endswith('.json') and not event.is_directory:
            print(f"New JSON file created: {event.src_path}")
            ingest_json_data(event.src_path)

    def on_modified(self, event):
        print(f"Event detected: type={event.event_type}, path={event.src_path}, is_directory={event.is_directory}")
        if event.src_path.endswith('.json') and not event.is_directory:
            print(f"JSON file modified: {event.src_path}")
            ingest_json_data(event.src_path)

def watch_landing_zone():
    if not os.path.exists(LANDING_ZONE):
        os.makedirs(LANDING_ZONE)
        print(f"Created directory: {LANDING_ZONE}")
    
    init_db()
    print("Database tables initialized.")

    event_handler = JSONFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=LANDING_ZONE, recursive=False)
    observer.start()
    print(f"Monitoring {LANDING_ZONE} for new JSON files...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_landing_zone()