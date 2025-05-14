from typing import List, Optional
from pydantic import BaseModel

class Food(BaseModel):
    name: str
    categories: str
    cuisines: str
    address: str
    rating_avg: Optional[float] = None
    rating_total_review: Optional[int] = None
    is_open: bool
    city_id: int
