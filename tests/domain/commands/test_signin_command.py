import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.signin_command import SignInCommand


class TestSignInCommand(unittest.TestCase):
    def test_signin_command_fields(self):
        cmd = SignInCommand(password="Pass1234", phone="3001234567")
        self.assertIsInstance(cmd, BaseCommand)
        self.assertEqual(cmd.password, "Pass1234")
        self.assertEqual(cmd.phone, "3001234567")

