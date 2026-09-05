from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand


@dataclass
class SignInCommand(BaseCommand):
    password: str
    phone: str
