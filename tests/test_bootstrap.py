import unittest
from unittest.mock import MagicMock

from app.adapters.message_bus import MessageBus
from app.bootstrap import _inject_dependencies, bootstrap
from app.domain.commands.base_command import BaseCommand


class _DummyCommand(BaseCommand[str]):
    value: str


class TestBootstrap(unittest.TestCase):
    def test_inject_dependencies_injects_matching_parameters(self):
        mock_container = MagicMock()
        mock_bus = MagicMock()
        called_with = {}

        def sample_handler(cmd, message_bus, container):
            called_with["cmd"] = cmd
            called_with["message_bus"] = message_bus
            called_with["container"] = container
            return "ok"

        injected = _inject_dependencies(
            sample_handler,
            {"container": mock_container, "unused_dep": "ignored"},
        )
        cmd = _DummyCommand()
        result = injected(cmd, mock_bus)

        self.assertEqual(result, "ok")
        self.assertEqual(called_with["cmd"], cmd)
        self.assertEqual(called_with["message_bus"], mock_bus)
        self.assertEqual(called_with["container"], mock_container)

    def test_bootstrap_returns_configured_message_bus(self):
        mock_container = MagicMock()
        bus = bootstrap(container=mock_container)

        self.assertIsInstance(bus, MessageBus)
        self.assertEqual(bus._container, mock_container)
        self.assertTrue(len(bus._command_handlers) > 0)

