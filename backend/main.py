from fastapi import FastAPI, Depends
from database import get_db, init_db
from sqlalchemy.orm import Session
from database import LocationDB, FoodDB

app = FastAPI()

init_db()

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {"status": "Backend is running"}

@app.get("/locations")
async def get_locations(db: Session = Depends(get_db)):
    locations = db.query(LocationDB).all()
    return [{"id": loc.id, "city_id": loc.city_id, "country_id": loc.country_id, "name": loc.name, "country_name": loc.country_name} for loc in locations]

@app.get("/foods")
async def get_foods(db: Session = Depends(get_db)):
    foods = db.query(FoodDB).all()
    return [{"id": food.id, "name": food.name, "categories": food.categories, "cuisines": food.cuisines, "address": food.address, "rating_avg": food.rating_avg, "rating_total_review": food.rating_total_review, "is_open": food.is_open, "city_id": food.city_id} for food in foods]