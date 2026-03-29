from pydantic import BaseModel
from typing import List
from clients.search_api.location import Location

class Response (BaseModel):
    locations: List[Location]
