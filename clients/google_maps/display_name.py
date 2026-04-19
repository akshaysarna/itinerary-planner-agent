from typing import Optional
from pydantic import BaseModel

class DisplayName(BaseModel):
    text: Optional[str] = None
    languageCode: Optional[str] = None