from pydantic import BaseModel
from clients.search_api.airport import Airport
from typing import List

class Location (BaseModel):
    type: str = ""
    airports: List[Airport] = []