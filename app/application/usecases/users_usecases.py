from app.domain.commands.get_all_users_paginated_command import GetAllUsersPaginatedCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.exceptions.bad_request_exception import BadRequestException
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

    @staticmethod
    def get_all_paginated(
            cmd: GetAllUsersPaginatedCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[list[UserModel], int, int]:
        if cmd.current_page < 1:
            raise BadRequestException("Current page is invalid")

        with container.unit_of_work() as uow:
            total_count = uow.user_repository.count()

            max_pages = total_count // cmd.limit
            if total_count % cmd.limit != 0:
                max_pages += 1

            if cmd.current_page > max_pages:
                return [], total_count, max_pages

            users = uow.user_repository.get_many(
                limit=cmd.limit,
                offset=(cmd.current_page - 1) * cmd.limit,
            )

            return users, total_count, max_pages
