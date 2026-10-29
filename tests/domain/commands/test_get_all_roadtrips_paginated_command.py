import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand


class TestGetAllRoadtripsPaginatedCommand(unittest.TestCase):
    def test_get_all_roadtrips_paginated_command_fields(self):
        cmd = GetAllRoadtripsPaginatedCommand(current_page=2, limit=10)
        self.assertIsInstance(cmd, BaseCommand)
        self.assertEqual(cmd.current_page, 2)
        self.assertEqual(cmd.limit, 10)

