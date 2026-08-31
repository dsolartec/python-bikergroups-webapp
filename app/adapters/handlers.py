from typing import Callable, Type

from app.application.usecases.auth_usecases import AuthUseCases
from app.domain.commands.base_command import BaseCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand


COMMAND_HANDLERS: dict[Type[BaseCommand], Callable] = {
    SignInCommand: AuthUseCases.signin,
    SignUpCommand: AuthUseCases.signup,
}
