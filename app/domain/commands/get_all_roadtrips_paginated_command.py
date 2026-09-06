from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand
from app.domain.models.roadtrip_model import RoadTripModel


@dataclass
class GetAllRoadtripsPaginatedCommand(BaseCommand[tuple[list[RoadTripModel], int, int]]):
    current_page: int
    limit: int
