from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand
from app.domain.models.user_model import UserModel


@dataclass
class GetUserByIDCommand(BaseCommand[UserModel]):
    id: str
    with_permissions: bool = False
