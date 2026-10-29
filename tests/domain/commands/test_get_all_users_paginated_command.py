import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.get_all_users_paginated_command import GetAllUsersPaginatedCommand


class TestGetAllUsersPaginatedCommand(unittest.TestCase):
    def test_get_all_users_paginated_command_fields(self):
        cmd = GetAllUsersPaginatedCommand(current_page=1, limit=15)
        self.assertIsInstance(cmd, BaseCommand)
        self.assertEqual(cmd.current_page, 1)
        self.assertEqual(cmd.limit, 15)

