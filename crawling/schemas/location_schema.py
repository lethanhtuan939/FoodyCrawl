from pydantic import BaseModel

class Location(BaseModel):
    city_id: int
    country_id: int
    name: str
    country_name: str