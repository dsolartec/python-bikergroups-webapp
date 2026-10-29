from datetime import datetime
import unittest
from uuid import UUID

from app.adapters.outputs.datasources.postgresql_entities.permission_entity import PermissionEntity
from app.adapters.outputs.datasources.postgresql_entities.user_entity import UserEntity
from app.adapters.outputs.datasources.postgresql_entities.user_permission_entity import UserPermissionEntity  # noqa: F401
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.models.user_model import UserModel


class TestUserEntity(unittest.TestCase):
    def test_from_model_and_to_model_with_permissions(self):
        user_id = "018f1234-5678-7000-8000-000000000001"
        perm_id = "018f1234-5678-7000-8000-000000000010"
        now = datetime(2026, 1, 1, 12, 0, 0)

        model = UserModel(
            id=user_id,
            phone="3001234567",
            password="hashed_password",
            display_name="Daniel",
            created_at=now,
            updated_at=now,
        )

        entity = UserEntity.from_model(model)
        entity.permissions = [
            PermissionEntity(
                id=UUID(perm_id),
                name=PermissionEnum.CAN_CREATE_ROADTRIP.value,
            )
        ]

        self.assertEqual(entity.id, UUID(user_id))
        self.assertEqual(entity.phone, "3001234567")
        self.assertEqual(entity.password, "hashed_password")

        converted = entity.to_model()
        self.assertEqual(converted.id, user_id)
        self.assertEqual(converted.phone, "3001234567")
        self.assertEqual(converted.display_name, "Daniel")
        self.assertEqual(len(converted.permissions), 1)
        self.assertEqual(converted.permissions[0].name, PermissionEnum.CAN_CREATE_ROADTRIP)

