from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand
from app.domain.models.user_model import UserModel


@dataclass
class SignInCommand(BaseCommand[UserModel]):
    password: str
    phone: str
