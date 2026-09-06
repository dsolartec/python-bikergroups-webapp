from dataclasses import dataclass
from datetime import datetime

from app.domain.commands.base_command import BaseCommand
from app.domain.models.coordinates_model import CoordinatesModel
from app.domain.models.roadtrip_model import RoadTripModel


@dataclass
class CreateOneRoadTripCommand(BaseCommand[RoadTripModel]):
    display_name: str

    start_at: datetime
    start_coordinates: CoordinatesModel

    end_coordinates: CoordinatesModel

    actor_id: str
