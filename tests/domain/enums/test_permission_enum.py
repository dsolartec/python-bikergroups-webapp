import unittest

from app.domain.enums.permission_enum import PermissionEnum


class TestPermissionEnum(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(PermissionEnum.CAN_CREATE_ROADTRIP.value, "create_roadtrip")
        self.assertEqual(PermissionEnum.CAN_UPDATE_ROADTRIP.value, "update_roadtrip")

