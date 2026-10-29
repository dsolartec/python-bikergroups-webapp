import unittest

from app.domain.enums.permission_enum import PermissionEnum
from app.domain.models.permission_model import PermissionModel
from app.domain.models.user_model import UserModel


class TestUserModel(unittest.TestCase):
    def test_user_model_excludes_password_and_permissions_on_dump(self):
        user = UserModel(
            id="user-1",
            phone="3001234567",
            password="secret-password",
            display_name="Rider",
            permissions=[
                PermissionModel(id="perm-1", name=PermissionEnum.CAN_CREATE_ROADTRIP)
            ],
        )

        self.assertEqual(user.password, "secret-password")
        self.assertEqual(len(user.permissions), 1)

        dumped = user.model_dump()
        self.assertNotIn("password", dumped)
        self.assertNotIn("permissions", dumped)
        self.assertEqual(dumped["phone"], "3001234567")
        self.assertEqual(dumped["display_name"], "Rider")

