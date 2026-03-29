from pydantic import BaseModel
from clients.google_maps.place import Place
from typing import List

class Response(BaseModel):
    places: List[Place] = []