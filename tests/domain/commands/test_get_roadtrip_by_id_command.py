import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.get_roadtrip_by_id_command import GetRoadTripByIDCommand


class TestGetRoadTripByIDCommand(unittest.TestCase):
    def test_get_roadtrip_by_id_command_fields(self):
        cmd = GetRoadTripByIDCommand(id="rt-123")
        self.assertIsInstance(cmd, BaseCommand)
        self.assertEqual(cmd.id, "rt-123")

