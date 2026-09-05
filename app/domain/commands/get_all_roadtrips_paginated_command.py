from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand


@dataclass
class GetAllRoadtripsPaginatedCommand(BaseCommand):
    current_page: int
    limit: int
