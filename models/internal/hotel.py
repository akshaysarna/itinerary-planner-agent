from pydantic import BaseModel
from models.internal.location import Location

class Hotel(BaseModel):
    name: str
    address : str
    rating: float
    coordinates: Location