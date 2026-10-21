from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand


@dataclass
class GetAdminStatsCommand(BaseCommand[tuple[int, int]]):
    pass
