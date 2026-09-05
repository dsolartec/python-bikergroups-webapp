from abc import ABC, abstractmethod
from typing import Any, Callable, Type

from app.domain.commands.base_command import BaseCommand
from app.domain.ports.abstract_container import AbstractContainer


class AbstractMessageBus(ABC):
    _container: AbstractContainer
    _command_handlers: dict[Type[BaseCommand], Callable]

    @abstractmethod
    def _handle_command(self, command: BaseCommand) -> Any:
        raise NotImplementedError

    def handle(self, message: BaseCommand) -> Any:
        if isinstance(message, BaseCommand):
            return self._handle_command(message)

        raise Exception(f"{message} is not a command.")
