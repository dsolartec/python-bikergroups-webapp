from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand


@dataclass
class RefreshTokenCommand(BaseCommand):
    refresh_token: str
