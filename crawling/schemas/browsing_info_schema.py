from pydantic import BaseModel
from typing import List

class BrowsingInfosRequest(BaseModel):
    delivery_ids: List[int]
    city_id: int = 217
    sort_type: int = 2
    root_category: int = 1000000
    root_category_ids: List[int] = [1000000]