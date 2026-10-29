import unittest
import pytest

from app.domain.commands.base_command import BaseCommand
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class _ConcreteMessageBus(AbstractMessageBus):
    def _handle_command(self, command):
        return "handled"


class TestAbstractMessageBus(unittest.TestCase):
    def test_cannot_instantiate_abstract_message_bus_directly(self):
        with pytest.raises(TypeError):
            AbstractMessageBus()  # type: ignore

    def test_handle_calls_handle_command_for_base_command(self):
        bus = _ConcreteMessageBus()
        self.assertEqual(bus.handle(BaseCommand()), "handled")

    def test_handle_raises_for_invalid_message(self):
        bus = _ConcreteMessageBus()
        with pytest.raises(Exception, match="is not a command"):
            bus.handle("invalid")  # type: ignore

