from dataclasses import dataclass
from datetime import datetime

from app.domain.commands.base_command import BaseCommand
from app.domain.models.coordinates_model import CoordinatesModel


@dataclass
class CreateOneRoadTripCommand(BaseCommand):
    display_name: str

    start_at: datetime
    start_coordinates: CoordinatesModel

    end_coordinates: CoordinatesModel

    actor_id: str
