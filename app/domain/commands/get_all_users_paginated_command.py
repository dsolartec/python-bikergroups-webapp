from dataclasses import dataclass

from app.domain.commands.base_command import BaseCommand
from app.domain.models.user_model import UserModel


@dataclass
class GetAllUsersPaginatedCommand(BaseCommand[tuple[list[UserModel], int, int]]):
    current_page: int
    limit: int
