from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.models.user_model import UserModel
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class UsersUseCases:
    @staticmethod
    def get_by_id(
            cmd: GetUserByIDCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> UserModel:
        with container.unit_of_work() as uow:
            return uow.user_repository.get_by_id(cmd.id, with_permissions=cmd.with_permissions)
