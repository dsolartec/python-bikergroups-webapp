import unittest
import pytest

from app.domain.ports.repositories.audit_log_repository import AuditLogRepository


class TestAuditLogRepositoryPort(unittest.TestCase):
    def test_cannot_instantiate_audit_log_repository_directly(self):
        with pytest.raises(TypeError):
            AuditLogRepository()  # type: ignore

