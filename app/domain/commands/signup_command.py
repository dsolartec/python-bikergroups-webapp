from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand


@dataclass
class SignUpCommand(BaseCommand):
    display_name: str
    password: str
    phone: str
