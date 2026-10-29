from datetime import datetime
import unittest
from unittest.mock import MagicMock

import pytest

from app.application.usecases.auth_usecases import AuthUseCases
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.wrong_credentials_exception import WrongCredentialsException
from app.domain.models.user_model import UserModel


class TestAuthUseCases(unittest.TestCase):
    def setUp(self):
        self.mock_uow = MagicMock()
        self.mock_uow.__enter__.return_value = self.mock_uow

        self.mock_encription = MagicMock()
        self.mock_container = MagicMock()
        self.mock_container.unit_of_work.return_value = self.mock_uow
        self.mock_container.encription.return_value = self.mock_encription
        self.mock_bus = MagicMock()

        self.user = UserModel(
            id="018f1234-5678-7000-8000-000000000001",
            phone="3001234567",
            password="hashed_password",
            display_name="Rider",
            created_at=datetime(2026, 1, 1, 10, 0, 0),
            updated_at=datetime(2026, 1, 1, 10, 0, 0),
        )

    def test_signin_success_returns_user_and_saves_audit_log(self):
        self.mock_uow.user_repository.get_by_phone.return_value = self.user
        self.mock_encription.verify_hash_password.return_value = True

        cmd = SignInCommand(phone="3001234567", password="Password123")
        result = AuthUseCases.signin(cmd, self.mock_bus, self.mock_container)

        self.assertEqual(result, self.user)
        self.mock_uow.user_repository.get_by_phone.assert_called_once_with(
            "3001234567", with_permissions=True
        )
        self.mock_encription.verify_hash_password.assert_called_once_with(
            "hashed_password", "Password123"
        )
        self.mock_uow.audit_log_repository.save.assert_called_once()
        saved_log = self.mock_uow.audit_log_repository.save.call_args[0][0]
        self.assertEqual(saved_log.actor_id, self.user.id)
        self.assertEqual(saved_log.action, AuditLogActionEnum.SIGN_IN)

    def test_signin_raises_wrong_credentials_when_user_not_found(self):
        self.mock_uow.user_repository.get_by_phone.side_effect = NotFoundException("User not found")
        cmd = SignInCommand(phone="3000000000", password="Password123")

        with pytest.raises(WrongCredentialsException):
            AuthUseCases.signin(cmd, self.mock_bus, self.mock_container)

    def test_signin_raises_wrong_credentials_when_password_invalid(self):
        self.mock_uow.user_repository.get_by_phone.return_value = self.user
        self.mock_encription.verify_hash_password.return_value = False
        cmd = SignInCommand(phone="3001234567", password="BadPassword")

        with pytest.raises(WrongCredentialsException):
            AuthUseCases.signin(cmd, self.mock_bus, self.mock_container)

    def test_signup_hashes_password_saves_user_and_audit_log(self):
        self.mock_encription.hash_password.return_value = "new_hashed_password"
        self.mock_uow.user_repository.save.return_value = self.user

        cmd = SignUpCommand(
            display_name="Rider",
            phone="3001234567",
            password="Password123",
        )
        result = AuthUseCases.signup(cmd, self.mock_bus, self.mock_container)

        self.assertEqual(result, self.user)
        self.mock_encription.hash_password.assert_called_once_with("Password123")
        self.mock_uow.user_repository.save.assert_called_once()
        self.mock_uow.audit_log_repository.save.assert_called_once()
        saved_log = self.mock_uow.audit_log_repository.save.call_args[0][0]
        self.assertEqual(saved_log.actor_id, self.user.id)
        self.assertEqual(saved_log.action, AuditLogActionEnum.SIGN_UP)

