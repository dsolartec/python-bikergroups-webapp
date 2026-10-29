import unittest
from unittest.mock import MagicMock, patch

from app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_permission_repository import (
    PostgreSQLUserPermissionRepository,
)
from app.domain.models.user_permission_model import UserPermissionModel


class TestPostgreSQLUserPermissionRepository(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.repo = PostgreSQLUserPermissionRepository(self.mock_session)

    @patch("app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_permission_repository.UserPermissionEntity")
    def test_save_returns_true(self, mock_entity_cls):
        model = UserPermissionModel(
            permission_id="018f1234-5678-7000-8000-000000000010",
            user_id="018f1234-5678-7000-8000-000000000001",
        )
        mock_entity = MagicMock()
        mock_entity_cls.from_model.return_value = mock_entity

        result = self.repo.save(model)

        self.assertTrue(result)
        self.mock_session.add.assert_called_once_with(mock_entity)
        self.mock_session.commit.assert_called_once()

