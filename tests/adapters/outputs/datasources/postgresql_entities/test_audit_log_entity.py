from datetime import datetime
import unittest
from uuid import UUID

from app.adapters.outputs.datasources.postgresql_entities.audit_log_entity import AuditLogEntity
from app.adapters.outputs.datasources.postgresql_entities.user_entity import UserEntity  # noqa: F401
from app.adapters.outputs.datasources.postgresql_entities.user_permission_entity import UserPermissionEntity  # noqa: F401
from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.models.audit_log_model import AuditLogModel


class TestAuditLogEntity(unittest.TestCase):
    def test_from_model_and_to_model(self):
        log_id = "018f1234-5678-7000-8000-000000000001"
        actor_id = "018f1234-5678-7000-8000-000000000002"
        now = datetime(2026, 5, 10, 12, 0, 0)

        model = AuditLogModel(
            id=log_id,
            actor_id=actor_id,
            action=AuditLogActionEnum.SIGN_IN,
            metadata={"ip": "127.0.0.1"},
            created_at=now,
        )

        entity = AuditLogEntity.from_model(model)

        self.assertEqual(entity.id, UUID(log_id))
        self.assertEqual(entity.actor_id, UUID(actor_id))
        self.assertEqual(entity.action, "sign_in")
        self.assertEqual(entity.action_metadata, {"ip": "127.0.0.1"})

        converted_model = entity.to_model()
        self.assertEqual(converted_model.id, log_id)
        self.assertEqual(converted_model.actor_id, actor_id)
        self.assertEqual(converted_model.action, AuditLogActionEnum.SIGN_IN)
        self.assertEqual(converted_model.metadata, {"ip": "127.0.0.1"})
        self.assertEqual(converted_model.created_at, now)

