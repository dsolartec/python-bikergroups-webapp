from datetime import datetime

from pydantic import BaseModel

from app.domain.models.coordinates_model import CoordinatesModel


class RoadTripModel(BaseModel):
    id: str | None
    display_name: str

    start_at: datetime
    start_coordinates: CoordinatesModel

    end_coordinates: CoordinatesModel

    # System properties

    created_at: datetime | None
    created_by: str | None

    updated_at: datetime | None
    updated_by: str | None
