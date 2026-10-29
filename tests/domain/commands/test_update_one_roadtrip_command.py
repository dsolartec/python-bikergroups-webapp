from datetime import datetime
import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.update_one_roadtrip_command import UpdateOneRoadTripCommand
from app.domain.models.coordinates_model import CoordinatesModel


class TestUpdateOneRoadTripCommand(unittest.TestCase):
    def test_update_one_roadtrip_command_fields(self):
        start_at = datetime(2026, 12, 1, 8, 0, 0)
        start_coords = CoordinatesModel(latitude=6.24, longitude=-75.58, name="Medellín")
        end_coords = CoordinatesModel(latitude=6.15, longitude=-75.37, name="Rionegro")

        cmd = UpdateOneRoadTripCommand(
            roadtrip_id="rt-1",
            display_name="Rodada Editada",
            start_at=start_at,
            start_coordinates=start_coords,
            end_coordinates=end_coords,
            actor_id="actor-1",
        )

        self.assertIsInstance(cmd, BaseCommand)
        self.assertEqual(cmd.roadtrip_id, "rt-1")
        self.assertEqual(cmd.display_name, "Rodada Editada")
        self.assertEqual(cmd.start_at, start_at)
        self.assertEqual(cmd.start_coordinates, start_coords)
        self.assertEqual(cmd.end_coordinates, end_coords)
        self.assertEqual(cmd.actor_id, "actor-1")

