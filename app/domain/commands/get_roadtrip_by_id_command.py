from dataclasses import dataclass
from typing import Optional

from app.domain.commands.base_command import BaseCommand
from app.domain.models.roadtrip_model import RoadTripModel


@dataclass
class GetRoadTripByIDCommand(BaseCommand[Optional[RoadTripModel]]):
    id: str
