import unittest
import pytest

from app.domain.ports.repositories.roadtrip_repository import RoadTripRepository


class TestRoadTripRepositoryPort(unittest.TestCase):
    def test_cannot_instantiate_roadtrip_repository_directly(self):
        with pytest.raises(TypeError):
            RoadTripRepository()  # type: ignore

