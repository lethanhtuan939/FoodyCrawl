import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from pydantic import ValidationError

from database import engine, SessionLocal, LocationDB, FoodDB, init_db
from models import Food, Location

# Đường dẫn đến thư mục landing_zone
LANDING_ZONE = "/app/landing_zone"

# Function to ingest data into database
def ingest_json_data(file_path):
    try:
        # Đọc file JSON
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        print(f"New JSON file detected: {os.path.basename(file_path)} with {len(data)} records")

        # Sử dụng session để chèn Location trước
        db = SessionLocal()
        try:
            for item in data:
                try:
                    # Ánh xạ và chèn Location trước
                    location_data = item.get("location", {})
                    if location_data:
                        location = Location(**location_data)
                        location_db = LocationDB(
                            id=location.id,
                            city_id=location.city_id,
                            country_id=location.CountryId,
                            name=location.Name,
                            country_name=location.CountryName
                        )
                        db.merge(location_db)
                        db.commit()  # Commit ngay để đảm bảo Location được lưu
                        print(f"Inserted/Updated location with city_id: {location.city_id}")
                    else:
                        print(f"No location data found in item: {item}")
                        continue

                    # Ánh xạ và chèn Food
                    food_data = {k: v for k, v in item.items() if k != "location"}
                    food = Food(**food_data)

                    # Kiểm tra xem city_id có tồn tại trong bảng locations không
                    existing_location = db.query(LocationDB).filter(LocationDB.city_id == food.city_id).first()
                    if not existing_location:
                        print(f"City ID {food.city_id} not found in locations table, skipping food item.")
                        continue

                    food_db = FoodDB(
                        id=food.id,
                        name=food.name,
                        categories=food.categories,
                        cuisines=food.cuisines,
                        address=food.address,
                        rating_avg=food.rating_avg,
                        rating_total_review=food.rating_total_review,
                        is_open=food.is_open,
                        city_id=food.city_id
                    )
                    db.merge(food_db)
                    db.commit()  # Commit sau khi chèn Food
                    print(f"Inserted/Updated food with id: {food.id}")

                except ValidationError as ve:
                    print(f"Validation error for item in {file_path}: {str(ve)}")
                    continue
                except Exception as e:
                    print(f"Error processing item in {file_path}: {str(e)}")
                    continue

            print(f"Successfully ingested data from {file_path} into database at {datetime.now()}")

        finally:
            db.close()

    except Exception as e:
        print(f"Error reading JSON file {file_path}: {str(e)}")

# Watchdog event handler to monitor landing_zone
class JSONFileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.json') and event.is_directory is False:
            print(f"New JSON file created: {event.src_path}")
            ingest_json_data(event.src_path)

    def on_modified(self, event):
        if event.src_path.endswith('.json') and event.is_directory is False:
            print(f"JSON file modified: {event.src_path}")
            ingest_json_data(event.src_path)

# Set up the file observer
def watch_landing_zone():
    # Kiểm tra và tạo thư mục nếu chưa tồn tại
    if not os.path.exists(LANDING_ZONE):
        os.makedirs(LANDING_ZONE)
        print(f"Created directory: {LANDING_ZONE}")
    
    # Tạo bảng nếu chưa tồn tại
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