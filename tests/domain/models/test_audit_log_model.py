from datetime import datetime
import unittest

from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.models.audit_log_model import AuditLogModel


class TestAuditLogModel(unittest.TestCase):
    def test_audit_log_model_defaults_and_serialization(self):
        dt = datetime(2026, 6, 1, 14, 0, 0)
        model = AuditLogModel(
            actor_id="user-1",
            action=AuditLogActionEnum.SIGN_IN,
            created_at=dt,
        )

        self.assertIsNone(model.id)
        self.assertIsNone(model.metadata)
        dumped = model.model_dump()
        self.assertEqual(dumped["actor_id"], "user-1")
        self.assertEqual(dumped["action"], AuditLogActionEnum.SIGN_IN)
        self.assertEqual(dumped["created_at"], "2026-06-01 14:00:00")

