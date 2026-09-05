from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand


@dataclass
class UpdateRoadTripPhotoCommand(BaseCommand):
    actor_id: str
    roadtrip_id: str
