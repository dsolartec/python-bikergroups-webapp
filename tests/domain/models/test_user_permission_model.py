import unittest

from app.domain.models.user_permission_model import UserPermissionModel


class TestUserPermissionModel(unittest.TestCase):
    def test_user_permission_model_fields(self):
        model = UserPermissionModel(
            permission_id="perm-1",
            user_id="user-1",
        )
        self.assertIsNone(model.id)
        self.assertEqual(model.permission_id, "perm-1")
        self.assertEqual(model.user_id, "user-1")

