from pydantic import BaseModel, Field
from typing import Optional, List

class Food(BaseModel):
    id: int
    name: str
    categories: List[str] = Field(default_factory=list)
    cuisines: List[str] = Field(default_factory=list)
    address: str
    rating_avg: float
    rating_total_review: int
    is_open: bool
    city_id: int

    class Config:
        orm_mode = True
        
class Location(BaseModel):
    id: int
    city_id: int
    countryId: int
    name: str
    countryName: str

    class Config:
        orm_mode = True