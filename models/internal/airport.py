from typing import Optional
from pydantic import BaseModel
from models.internal.location import Location

class Airport(BaseModel):
    airport_code: str
    address: str
    name: str
    coordinates: Optional[Location]
