import inspect
from typing import Callable

from app.adapters.container import Container
from app.adapters.handlers import COMMAND_HANDLERS
from app.adapters.message_bus import MessageBus
from app.domain.ports.abstract_container import AbstractContainer


def _inject_dependencies(handler: Callable, dependencies: dict):
    params = inspect.signature(handler).parameters

    args = {
        name: dependency
            for name, dependency in dependencies.items()
                if name in params
    }

    return lambda cmd, message_bus: handler(cmd, message_bus, **args)

def bootstrap(
        container: AbstractContainer = Container(),
) -> MessageBus:
    dependencies = {"container": container}

    injected_command_handlers = {
        command_type: _inject_dependencies(handler, dependencies)
            for command_type, handler in COMMAND_HANDLERS.items()
    }
    
    return MessageBus(container, injected_command_handlers)
