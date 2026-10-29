import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand


class TestGetUserByIDCommand(unittest.TestCase):
    def test_get_user_by_id_command_defaults_and_fields(self):
        cmd1 = GetUserByIDCommand(id="user-1")
        self.assertIsInstance(cmd1, BaseCommand)
        self.assertEqual(cmd1.id, "user-1")
        self.assertFalse(cmd1.with_permissions)

        cmd2 = GetUserByIDCommand(id="user-1", with_permissions=True)
        self.assertTrue(cmd2.with_permissions)

