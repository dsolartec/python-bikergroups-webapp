from datetime import datetime
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from psycopg2.errors import UniqueViolation
import pytest
from sqlalchemy.exc import IntegrityError

from app.adapters.outputs.datasources.postgresql_entities.user_permission_entity import UserPermissionEntity  # noqa: F401
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_repository import (
    PostgreSQLUserRepository,
)
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.phone_already_exists_exception import PhoneAlreadyExistsException
from app.domain.models.user_model import UserModel


class _FakeUniqueViolation(UniqueViolation):
    @property
    def pgcode(self):
        return "23505"

    @property
    def diag(self):
        return SimpleNamespace(constraint_name="users_phone_key")


class TestPostgreSQLUserRepository(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.repo = PostgreSQLUserRepository(self.mock_session)
        self.sample_user = UserModel(
            id="018f1234-5678-7000-8000-000000000001",
            phone="3001234567",
            password="hashed_password",
            display_name="Rider",
            created_at=datetime(2026, 1, 1, 10, 0, 0),
            updated_at=datetime(2026, 1, 1, 10, 0, 0),
        )

    def test_count(self):
        self.mock_session.scalar.return_value = 15
        self.assertEqual(self.repo.count(), 15)

        self.mock_session.scalar.return_value = None
        self.assertEqual(self.repo.count(), 0)

    def test_get_by_id_found(self):
        mock_entity = MagicMock()
        mock_entity.to_model.return_value = self.sample_user
        self.mock_session.scalar.return_value = mock_entity

        result = self.repo.get_by_id("018f1234-5678-7000-8000-000000000001", with_permissions=True)
        self.assertEqual(result, self.sample_user)

    def test_get_by_id_not_found(self):
        self.mock_session.scalar.return_value = None
        with pytest.raises(NotFoundException, match="User not found"):
            self.repo.get_by_id("018f1234-5678-7000-8000-000000000001")

    def test_get_by_phone_found(self):
        mock_entity = MagicMock()
        mock_entity.to_model.return_value = self.sample_user
        self.mock_session.scalar.return_value = mock_entity

        result = self.repo.get_by_phone("3001234567", with_permissions=True)
        self.assertEqual(result, self.sample_user)

    def test_get_by_phone_not_found(self):
        self.mock_session.scalar.return_value = None
        with pytest.raises(NotFoundException, match="User not found"):
            self.repo.get_by_phone("3001234567")

    def test_get_many(self):
        mock_entity = MagicMock()
        mock_entity.to_model.return_value = self.sample_user
        self.mock_session.scalars.return_value.all.return_value = [mock_entity]

        result = self.repo.get_many(limit=10, offset=0)
        self.assertEqual(result, [self.sample_user])

    @patch("app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_repository.UserEntity")
    def test_save_success(self, mock_entity_cls):
        mock_entity = MagicMock()
        mock_entity.to_model.return_value = self.sample_user
        mock_entity_cls.from_model.return_value = mock_entity

        result = self.repo.save(self.sample_user)

        self.assertEqual(result, self.sample_user)
        self.mock_session.add.assert_called_once_with(mock_entity)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(mock_entity)

    @patch("app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_repository.UserEntity")
    def test_save_duplicate_phone_raises_phone_already_exists_exception(self, mock_entity_cls):
        mock_entity_cls.from_model.return_value = MagicMock()
        orig = _FakeUniqueViolation()
        self.mock_session.commit.side_effect = IntegrityError("stmt", {}, orig)

        with pytest.raises(PhoneAlreadyExistsException):
            self.repo.save(self.sample_user)

