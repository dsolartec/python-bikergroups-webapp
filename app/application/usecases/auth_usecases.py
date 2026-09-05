from app.domain.commands.refresh_command import RefreshTokenCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.unauthorized_exception import UnauthorizedException
from app.domain.exceptions.wrong_credentials_exception import WrongCredentialsException
from app.domain.models.audit_log_model import AuditLogModel
from app.domain.models.user_model import UserModel
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class AuthUseCases:
    @staticmethod
    def refresh(
        cmd: RefreshTokenCommand,
        message_bus: AbstractMessageBus,
        container: AbstractContainer,
    ) -> tuple[str, str]:
        authenticator = container.authenticator()

        with container.unit_of_work() as uow:
            refresh_token = authenticator.parse_refresh_token(token_string=cmd.refresh_token)

            try:
                user = uow.user_repository.get_by_id(refresh_token.user_id, with_permissions=True)
            except NotFoundException as nfe:
                raise UnauthorizedException("Invalid refresh token") from nfe

            access_token = authenticator.generate_access_token(
                permissions_names=[permission.name for permission in user.permissions],
                phone=user.phone,
                user_id=user.id,
            )

            return access_token, cmd.refresh_token

    @staticmethod
    def signin(
            cmd: SignInCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[str, str]:
        authenticator = container.authenticator()

        with container.unit_of_work() as uow:
            try:
                user = uow.user_repository.get_by_phone(cmd.phone, with_permissions=True)
            except NotFoundException as nfe:
                raise WrongCredentialsException() from nfe

            if not container.encription().verify_hash_password(user.password, cmd.password):
                raise WrongCredentialsException()

            access_token = authenticator.generate_access_token(
                permissions_names=[permission.name for permission in user.permissions],
                phone=user.phone,
                user_id=user.id,
            )

            refresh_token = authenticator.generate_refresh_token(user.id)

            uow.audit_log_repository.save(AuditLogModel(
                actor_id=user.id,
                action=AuditLogActionEnum.SIGN_IN,
            ))

            return access_token, refresh_token

    @staticmethod
    def signup(
            cmd: SignUpCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[str, str]:
        authenticator = container.authenticator()

        with container.unit_of_work() as uow:
            password_hash = container.encription().hash_password(cmd.password)

            user = uow.user_repository.save(UserModel(
                display_name=cmd.display_name,
                password=password_hash,
                phone=cmd.phone,
            ))

            access_token = authenticator.generate_access_token(
                permissions_names=[],
                phone=user.phone,
                user_id=user.id,
            )

            refresh_token = authenticator.generate_refresh_token(user.id)

            uow.audit_log_repository.save(AuditLogModel(
                actor_id=user.id,
                action=AuditLogActionEnum.SIGN_UP,
            ))

            return access_token, refresh_token
