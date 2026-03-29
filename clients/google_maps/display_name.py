from pydantic import BaseModel

class DisplayName(BaseModel):
    text: str = None
    languageCode: str = None