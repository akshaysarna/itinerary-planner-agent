from pydantic import BaseModel
from clients.google_maps.location import Location
from clients.google_maps.display_name import DisplayName

class Place(BaseModel):
    formattedAddress: str = ""
    rating: float = 0.0
    location: Location
    displayName: DisplayName

    @property
    def displayNameText(self):
        return self.displayName.text if self.displayName else ''