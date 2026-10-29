import unittest

from app.domain.models.coordinates_model import CoordinatesModel


class TestCoordinatesModel(unittest.TestCase):
    def test_coordinates_model_fields(self):
        coords = CoordinatesModel(
            latitude=6.2442,
            longitude=-75.5812,
            name="Medellín",
        )
        self.assertEqual(coords.latitude, 6.2442)
        self.assertEqual(coords.longitude, -75.5812)
        self.assertEqual(coords.name, "Medellín")

