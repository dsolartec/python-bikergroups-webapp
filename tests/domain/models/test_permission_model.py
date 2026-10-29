import unittest

from app.domain.enums.permission_enum import PermissionEnum
from app.domain.models.permission_model import PermissionModel


class TestPermissionModel(unittest.TestCase):
    def test_permission_model_fields(self):
        perm = PermissionModel(
            id="perm-1",
            name=PermissionEnum.CAN_CREATE_ROADTRIP,
        )
        self.assertEqual(perm.id, "perm-1")
        self.assertEqual(perm.name, PermissionEnum.CAN_CREATE_ROADTRIP)

