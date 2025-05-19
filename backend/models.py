from pydantic import BaseModel, Field
from typing import Optional, List

class Food(BaseModel):
    id: int
    name: str
    categories: str
    cuisines: str
    address: str
    rating_avg: Optional[float] = None
    rating_total_review: Optional[int] = None
    image_url: str
    is_open: bool
    city_id: int
        
class Location(BaseModel):
    id: int
    city_id: int
    country_id: int
    name: str
    country_name: str

    class Config:
        orm_mode = True