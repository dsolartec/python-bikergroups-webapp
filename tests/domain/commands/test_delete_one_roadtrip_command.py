import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.delete_one_roadtrip_command import DeleteOneRoadTripCommand


class TestDeleteOneRoadTripCommand(unittest.TestCase):
    def test_delete_one_roadtrip_command_fields(self):
        cmd = DeleteOneRoadTripCommand(actor_id="actor-1", roadtrip_id="rt-1")
        self.assertIsInstance(cmd, BaseCommand)
        self.assertEqual(cmd.actor_id, "actor-1")
        self.assertEqual(cmd.roadtrip_id, "rt-1")

