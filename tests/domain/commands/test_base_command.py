import unittest

from app.domain.commands.base_command import BaseCommand


class TestBaseCommand(unittest.TestCase):
    def test_base_command_instantiation(self):
        cmd = BaseCommand()
        self.assertIsInstance(cmd, BaseCommand)

