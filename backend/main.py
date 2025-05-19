from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import func, or_
from typing import Optional
from database import get_db, init_db
from sqlalchemy.orm import Session
from database import LocationDB, FoodDB
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FoodyCrawl Rest API",
    description="API for crawling food data from Foody.vn",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    root_path="/api/backend")
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

init_db()

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {"status": "Backend is running"}

@app.get("/locations")
async def get_locations(db: Session = Depends(get_db)):
    locations = db.query(LocationDB).all()
    return [{"id": loc.id, "city_id": loc.city_id, "country_id": loc.country_id, "name": loc.name, "country_name": loc.country_name} for loc in locations]

@app.get("/foods")
async def search_foods(
    query: Optional[str] = Query(None, min_length=1, description="Search term for name, categories, or cuisines"),
    city_id: Optional[int] = Query(None, ge=1, description="Filter by city ID"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Search foods by name, categories, cuisines, or city_id with pagination.
    """
    try:
        # Base query
        base_query = db.query(FoodDB)

        # Apply filters
        if query or city_id:
            filters = []

            # Search by query (name, categories, cuisines)
            if query:
                query_pattern = f"%{query}%"
                filters.append(
                    or_(
                        FoodDB.name.ilike(query_pattern),
                        func.array_to_string(FoodDB.categories, ",").ilike(query_pattern),
                        func.array_to_string(FoodDB.cuisines, ",").ilike(query_pattern)
                    )
                )

            # Filter by city_id
            if city_id:
                filters.append(FoodDB.city_id == city_id)

            # Combine filters with AND
            base_query = base_query.filter(*filters)

        # Get total count for pagination metadata
        total_items = base_query.count()

        # Apply pagination
        offset = (page - 1) * page_size
        foods = base_query.offset(offset).limit(page_size).all()

        # Format results
        results = [
            {
                "id": food.id,
                "name": food.name,
                "categories": food.categories,
                "cuisines": food.cuisines,
                "address": food.address,
                "rating_avg": food.rating_avg,
                "rating_total_review": food.rating_total_review,
                "image_url": food.image_url,
                "is_open": food.is_open,
                "city_id": food.city_id
            }
            for food in foods
        ]

        # Calculate total pages
        total_pages = (total_items + page_size - 1) // page_size

        return {
            "items": results,
            "total_items": total_items,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")