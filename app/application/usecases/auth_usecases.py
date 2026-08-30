from app.domain.commands.signup_command import SignUpCommand
from app.domain.models.user_model import UserModel
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class AuthUseCases:
    @staticmethod
    def signup(
            cmd: SignUpCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[str, str]:
        with container.unit_of_work() as uow:
            password_hash = container.encription().hash_password(cmd.password)

            user = uow.user_repository.save(UserModel(
                id=None,
                username=cmd.username,
                password=password_hash,

                display_name=cmd.display_name,

                created_at=None,
                updated_at=None,
            ))

            authenticator = container.authenticator()

            access_token = authenticator.generate_access_token(user.id, user.username)
            refresh_token = authenticator.generate_refresh_token(user.id)

            return access_token, refresh_token
