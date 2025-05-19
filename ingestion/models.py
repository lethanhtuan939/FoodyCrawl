from pydantic import BaseModel
from typing import Optional, List

class Location(BaseModel):
    id: int
    city_id: int
    country_id: int
    name: str
    country_name: str

class Food(BaseModel):
    id: int
    name: str
    categories: List[str]
    cuisines: List[str]
    address: str
    rating_avg: Optional[float] = None
    rating_total_review: Optional[int] = None
    image_url: str
    is_open: bool
    city_id: int