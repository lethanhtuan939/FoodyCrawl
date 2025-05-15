from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    id: int
    city_id: int
    CountryId: int
    Name: str
    CountryName: str

class Food(BaseModel):
    id: int
    name: str
    categories: List[str]
    cuisines: List[str]
    address: str
    rating_avg: float
    rating_total_review: int
    is_open: bool
    city_id: int