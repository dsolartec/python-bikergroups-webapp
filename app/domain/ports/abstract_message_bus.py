from abc import ABC, abstractmethod
from typing import Callable, Type

from app.domain.commands.base_command import BaseCommand
from app.domain.ports.abstract_container import AbstractContainer


class AbstractMessageBus(ABC):
    _container: AbstractContainer
    _command_handlers: dict[Type[BaseCommand], Callable]

    @abstractmethod
    def _handle_command[T](self, command: BaseCommand[T]) -> T:
        raise NotImplementedError

    def handle[T](self, message: BaseCommand[T]) -> T:
        if isinstance(message, BaseCommand):
            return self._handle_command(message)

        raise Exception(f"{message} is not a command.")
