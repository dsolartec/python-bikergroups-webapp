import unittest
from uuid import UUID

from app.adapters.outputs.datasources.postgresql_entities.permission_entity import PermissionEntity
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.models.permission_model import PermissionModel


class TestPermissionEntity(unittest.TestCase):
    def test_from_model_and_to_model(self):
        perm_id = "018f1234-5678-7000-8000-000000000010"
        model = PermissionModel(
            id=perm_id,
            name=PermissionEnum.CAN_CREATE_ROADTRIP,
        )

        entity = PermissionEntity.from_model(model)
        self.assertEqual(entity.id, UUID(perm_id))
        self.assertEqual(entity.name, "create_roadtrip")

        converted = entity.to_model()
        self.assertEqual(converted.id, perm_id)
        self.assertEqual(converted.name, PermissionEnum.CAN_CREATE_ROADTRIP)

