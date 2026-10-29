import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.update_roadtrip_photo_command import UpdateRoadTripPhotoCommand


class TestUpdateRoadTripPhotoCommand(unittest.TestCase):
    def test_update_roadtrip_photo_command_fields(self):
        cmd = UpdateRoadTripPhotoCommand(actor_id="actor-1", roadtrip_id="rt-1")
        self.assertIsInstance(cmd, BaseCommand)
        self.assertEqual(cmd.actor_id, "actor-1")
        self.assertEqual(cmd.roadtrip_id, "rt-1")

