from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.models.coordinates_model import CoordinatesModel


class CreateOneRoadTripRequestBody(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    display_name: str = Field(min_length=8, max_length=120)

    start_at: datetime
    start_coordinates: CoordinatesModel

    end_coordinates: CoordinatesModel
