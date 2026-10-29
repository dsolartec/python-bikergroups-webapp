from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch

from app.adapters.outputs.datasources.postgresql_repositories.postgresql_audit_log_repository import (
    PostgreSQLAuditLogRepository,
)
from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.models.audit_log_model import AuditLogModel


class TestPostgreSQLAuditLogRepository(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.repo = PostgreSQLAuditLogRepository(self.mock_session)

    @patch("app.adapters.outputs.datasources.postgresql_repositories.postgresql_audit_log_repository.AuditLogEntity")
    def test_save_success(self, mock_entity_cls):
        log_model = AuditLogModel(
            actor_id="018f1234-5678-7000-8000-000000000001",
            action=AuditLogActionEnum.SIGN_IN,
        )
        saved_model = AuditLogModel(
            id="018f1234-5678-7000-8000-000000000099",
            actor_id="018f1234-5678-7000-8000-000000000001",
            action=AuditLogActionEnum.SIGN_IN,
            created_at=datetime(2026, 1, 1, 10, 0, 0),
        )

        mock_entity = MagicMock()
        mock_entity.to_model.return_value = saved_model
        mock_entity_cls.from_model.return_value = mock_entity

        result = self.repo.save(log_model)

        self.assertEqual(result, saved_model)
        self.mock_session.add.assert_called_once_with(mock_entity)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(mock_entity)

    @patch("app.adapters.outputs.datasources.postgresql_repositories.postgresql_audit_log_repository.AuditLogEntity")
    def test_save_returns_none_on_exception(self, mock_entity_cls):
        mock_entity_cls.from_model.side_effect = RuntimeError("Database error")
        log_model = AuditLogModel(
            actor_id="018f1234-5678-7000-8000-000000000001",
            action=AuditLogActionEnum.SIGN_IN,
        )

        result = self.repo.save(log_model)
        self.assertIsNone(result)

