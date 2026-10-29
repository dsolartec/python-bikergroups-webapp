import unittest
from unittest.mock import MagicMock, patch

from app.adapters.outputs.datasources.postgresql_repositories.postgresql_audit_log_repository import (
    PostgreSQLAuditLogRepository,
)
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_roadtrip_repository import (
    PostgreSQLRoadTripRepository,
)
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_permission_repository import (
    PostgreSQLUserPermissionRepository,
)
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_repository import (
    PostgreSQLUserRepository,
)
from app.adapters.outputs.datasources.unit_of_work import UnitOfWork


class TestUnitOfWork(unittest.TestCase):
    @patch("app.adapters.outputs.datasources.unit_of_work.scoped_session")
    @patch("app.adapters.outputs.datasources.unit_of_work.sessionmaker")
    @patch("app.adapters.outputs.datasources.unit_of_work.create_engine")
    def setUp(self, mock_create_engine, mock_sessionmaker, mock_scoped_session):
        self.mock_engine = MagicMock()
        self.mock_session = MagicMock()
        mock_create_engine.return_value = self.mock_engine
        mock_scoped_session.return_value = self.mock_session

        self.uow = UnitOfWork("user:pass@localhost:5432/db")

    def test_enter_initializes_repositories_and_exit_rolls_back_and_closes(self):
        with self.uow as uow:
            self.assertIsInstance(uow.audit_log_repository, PostgreSQLAuditLogRepository)
            self.assertIsInstance(uow.roadtrip_repository, PostgreSQLRoadTripRepository)
            self.assertIsInstance(uow.user_permission_repository, PostgreSQLUserPermissionRepository)
            self.assertIsInstance(uow.user_repository, PostgreSQLUserRepository)

        self.mock_session.rollback.assert_called_once()
        self.mock_session.close.assert_called_once()

    @patch("app.adapters.outputs.datasources.unit_of_work.BaseEntity")
    def test_generate_initial_data_creates_tables_and_permissions(self, mock_base_entity):
        self.uow.generate_initial_data()

        mock_base_entity.metadata.create_all.assert_called_once_with(self.mock_engine)
        self.mock_session.add_all.assert_called_once()
        self.mock_session.commit.assert_called_once()

