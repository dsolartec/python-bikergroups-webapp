from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand


@dataclass
class GetUserByIDCommand(BaseCommand):
    id: str
    with_permissions: bool = False
