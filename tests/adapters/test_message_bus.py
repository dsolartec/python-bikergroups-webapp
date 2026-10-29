import unittest
from unittest.mock import MagicMock

import pytest

from app.adapters.message_bus import MessageBus
from app.domain.commands.base_command import BaseCommand


class _SampleCommand(BaseCommand[int]):
    pass


class TestMessageBus(unittest.TestCase):
    def test_handle_dispatches_command_to_registered_handler(self):
        mock_container = MagicMock()
        mock_handler = MagicMock(return_value=42)
        bus = MessageBus(
            container=mock_container,
            command_handlers={_SampleCommand: mock_handler},
        )

        cmd = _SampleCommand()
        result = bus.handle(cmd)

        self.assertEqual(result, 42)
        mock_handler.assert_called_once_with(cmd, bus)

    def test_handle_raises_exception_for_non_command(self):
        mock_container = MagicMock()
        bus = MessageBus(container=mock_container, command_handlers={})

        with pytest.raises(Exception, match="is not a command"):
            bus.handle("not_a_command")  # type: ignore

