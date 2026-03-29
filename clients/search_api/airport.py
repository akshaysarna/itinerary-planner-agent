from pydantic import BaseModel


class Airport(BaseModel):
    title: str = ""
    airport_code: str = ""