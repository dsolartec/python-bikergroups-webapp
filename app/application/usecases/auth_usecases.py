from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.wrong_credentials_exception import WrongCredentialsException
from app.domain.models.user_model import UserModel
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class AuthUseCases:
    @staticmethod
    def signin(
            cmd: SignInCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[str, str]:
        with container.unit_of_work() as uow:
            try:
                user = uow.user_repository.get_by_username(cmd.username)
            except NotFoundException as nfe:
                raise WrongCredentialsException() from nfe

            if not container.encription().verify_hash_password(user.password, cmd.password):
                raise WrongCredentialsException()

            authenticator = container.authenticator()

            access_token = authenticator.generate_access_token(user.id, user.username)
            refresh_token = authenticator.generate_refresh_token(user.id)

            return access_token, refresh_token

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
