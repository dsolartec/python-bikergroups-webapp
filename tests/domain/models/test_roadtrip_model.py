from datetime import datetime
import unittest

from app.domain.models.coordinates_model import CoordinatesModel
from app.domain.models.roadtrip_model import RoadTripModel


class TestRoadTripModel(unittest.TestCase):
    def test_roadtrip_model_creation_and_dump(self):
        start_at = datetime(2026, 12, 1, 7, 30, 0)
        rt = RoadTripModel(
            display_name="Rodada Nocturna",
            start_at=start_at,
            start_coordinates=CoordinatesModel(latitude=6.24, longitude=-75.58, name="Medellín"),
            end_coordinates=CoordinatesModel(latitude=6.17, longitude=-75.59, name="Envigado"),
        )

        self.assertIsNone(rt.id)
        self.assertEqual(rt.display_name, "Rodada Nocturna")
        dumped = rt.model_dump()
        self.assertEqual(dumped["start_at"], "2026-12-01 07:30:00")
        self.assertEqual(dumped["start_coordinates"]["name"], "Medellín")

