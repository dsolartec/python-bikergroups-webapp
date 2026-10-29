import unittest
from uuid import UUID

from app.adapters.outputs.datasources.postgresql_entities.user_permission_entity import UserPermissionEntity
from app.domain.models.user_permission_model import UserPermissionModel


class TestUserPermissionEntity(unittest.TestCase):
    def test_from_model_and_to_model(self):
        up_id = "018f1234-5678-7000-8000-000000000050"
        perm_id = "018f1234-5678-7000-8000-000000000010"
        user_id = "018f1234-5678-7000-8000-000000000001"

        model = UserPermissionModel(
            id=up_id,
            permission_id=perm_id,
            user_id=user_id,
        )

        entity = UserPermissionEntity.from_model(model)
        self.assertEqual(entity.id, UUID(up_id))
        self.assertEqual(entity.permission_id, UUID(perm_id))
        self.assertEqual(entity.user_id, UUID(user_id))

        converted = entity.to_model()
        self.assertEqual(converted.id, up_id)
        self.assertEqual(converted.permission_id, perm_id)
        self.assertEqual(converted.user_id, user_id)

