import unittest

from app.domain.enums.audit_log_action_enum import AuditLogActionEnum


class TestAuditLogActionEnum(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(AuditLogActionEnum.SIGN_IN.value, "sign_in")
        self.assertEqual(AuditLogActionEnum.SIGN_UP.value, "sign_up")
        self.assertEqual(AuditLogActionEnum.ROADTRIP_CREATED.value, "roadtrip_created")
        self.assertEqual(
            AuditLogActionEnum.ROADTRIP_PHOTO_UPDATED.value,
            "roadtrip_photo_updated",
        )

