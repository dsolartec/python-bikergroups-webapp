from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.wrong_credentials_exception import WrongCredentialsException
from app.domain.models.audit_log_model import AuditLogModel
from app.domain.models.user_model import UserModel
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class AuthUseCases:
    @staticmethod
    def signin(
            cmd: SignInCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[UserModel]:
        with container.unit_of_work() as uow:
            try:
                user = uow.user_repository.get_by_phone(cmd.phone, with_permissions=True)
            except NotFoundException as nfe:
                raise WrongCredentialsException() from nfe

            if not container.encription().verify_hash_password(user.password, cmd.password):
                raise WrongCredentialsException()

            uow.audit_log_repository.save(AuditLogModel(
                actor_id=user.id,
                action=AuditLogActionEnum.SIGN_IN,
            ))

            return user

    @staticmethod
    def signup(
            cmd: SignUpCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[UserModel]:
        with container.unit_of_work() as uow:
            password_hash = container.encription().hash_password(cmd.password)

            user = uow.user_repository.save(UserModel(
                display_name=cmd.display_name,
                password=password_hash,
                phone=cmd.phone,
            ))

            uow.audit_log_repository.save(AuditLogModel(
                actor_id=user.id,
                action=AuditLogActionEnum.SIGN_UP,
            ))

            return user
