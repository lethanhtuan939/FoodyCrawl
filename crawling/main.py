from fastapi import FastAPI
import json
import os
from datetime import datetime

app = FastAPI()

LANDING_ZONE = "/app/landing_zone"
if not os.path.exists(LANDING_ZONE):
    os.makedirs(LANDING_ZONE)

# Dữ liệu JSON mẫu
SAMPLE_DATA = [
    {
        "id": 1,
        "name": "Pho Bo",
        "categories": ["Vietnamese", "Noodle"],
        "cuisines": ["Vietnamese"],
        "address": "123 Le Loi St, TP. HCM",
        "rating_avg": 4.5,
        "rating_total_review": 200,
        "is_open": True,
        "city_id": 217,
        "location": {
            "id": 1,
            "city_id": 217,
            "CountryId": 86,
            "Name": "TP. HCM",
            "CountryName": "Vietnam"
        }
    }
]

@app.get("/crawl")
async def crawl_data():
    try:
        # Tạo tên file dựa trên timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"food_{timestamp}.json"
        file_path = os.path.join(LANDING_ZONE, file_name)

        # Lưu dữ liệu vào file JSON
        with open(file_path, "w") as f:
            json.dump(SAMPLE_DATA, f, indent=4)

        return {"message": f"Successfully created JSON file: {file_name}"}

    except Exception as e:
        return {"error": f"Failed to create JSON file: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)