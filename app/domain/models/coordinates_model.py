from pydantic import BaseModel


class CoordinatesModel(BaseModel):
    latitude: float
    longitude: float
    name: str
