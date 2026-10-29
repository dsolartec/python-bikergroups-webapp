from datetime import datetime
import unittest
from uuid import UUID

from app.adapters.outputs.datasources.postgresql_entities.roadtrip_entity import RoadTripEntity
from app.adapters.outputs.datasources.postgresql_entities.user_entity import UserEntity  # noqa: F401
from app.adapters.outputs.datasources.postgresql_entities.user_permission_entity import UserPermissionEntity  # noqa: F401
from app.domain.models.coordinates_model import CoordinatesModel
from app.domain.models.roadtrip_model import RoadTripModel


class TestRoadTripEntity(unittest.TestCase):
    def test_from_model_and_to_model(self):
        rt_id = "018f1234-5678-7000-8000-000000000099"
        actor_id = "018f1234-5678-7000-8000-000000000001"
        start_at = datetime(2026, 12, 1, 8, 0, 0)
        created_at = datetime(2026, 10, 1, 8, 0, 0)

        model = RoadTripModel(
            id=rt_id,
            display_name="Rodada Santa Fe",
            start_at=start_at,
            start_coordinates=CoordinatesModel(latitude=6.24, longitude=-75.58, name="Medellín"),
            end_coordinates=CoordinatesModel(latitude=6.55, longitude=-75.82, name="Santa Fe"),
            created_at=created_at,
            created_by=actor_id,
            updated_at=created_at,
            updated_by=actor_id,
        )

        entity = RoadTripEntity.from_model(model)
        self.assertEqual(entity.id, UUID(rt_id))
        self.assertEqual(entity.display_name, "Rodada Santa Fe")
        self.assertEqual(entity.created_by, UUID(actor_id))
        self.assertEqual(entity.updated_by, UUID(actor_id))

        converted = entity.to_model()
        self.assertEqual(converted.id, rt_id)
        self.assertEqual(converted.display_name, "Rodada Santa Fe")
        self.assertEqual(converted.start_coordinates.name, "Medellín")
        self.assertEqual(converted.end_coordinates.name, "Santa Fe")
        self.assertEqual(converted.created_by, actor_id)

