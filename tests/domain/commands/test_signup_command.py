import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.signup_command import SignUpCommand


class TestSignUpCommand(unittest.TestCase):
    def test_signup_command_fields(self):
        cmd = SignUpCommand(
            display_name="Rider",
            password="Pass1234",
            phone="3001234567",
        )
        self.assertIsInstance(cmd, BaseCommand)
        self.assertEqual(cmd.display_name, "Rider")
        self.assertEqual(cmd.password, "Pass1234")
        self.assertEqual(cmd.phone, "3001234567")

