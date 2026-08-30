from typing import Callable, Type

from app.domain.commands.base_command import BaseCommand
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class MessageBus(AbstractMessageBus):
    def __init__(
            self,
            container: AbstractContainer,
            command_handlers: dict[Type[BaseCommand], Callable],
    ):
        self._container = container
        self._command_handlers = command_handlers

    def _handle_command(self, command: BaseCommand) -> any:
        handler = self._command_handlers[type(command)]
        return handler(command, self)
