from datetime import datetime
import unittest
from unittest.mock import MagicMock

import pytest

from app.application.usecases.users_usecases import UsersUseCases
from app.domain.commands.get_all_users_paginated_command import GetAllUsersPaginatedCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.exceptions.bad_request_exception import BadRequestException
from app.domain.models.user_model import UserModel


class TestUsersUseCases(unittest.TestCase):
    def setUp(self):
        self.mock_uow = MagicMock()
        self.mock_uow.__enter__.return_value = self.mock_uow

        self.mock_container = MagicMock()
        self.mock_container.unit_of_work.return_value = self.mock_uow
        self.mock_bus = MagicMock()

        self.user = UserModel(
            id="018f1234-5678-7000-8000-000000000001",
            phone="3001234567",
            display_name="Rider",
            created_at=datetime(2026, 1, 1, 10, 0, 0),
            updated_at=datetime(2026, 1, 1, 10, 0, 0),
        )

    def test_get_by_id_returns_user(self):
        self.mock_uow.user_repository.get_by_id.return_value = self.user
        cmd = GetUserByIDCommand(id=self.user.id, with_permissions=True)

        result = UsersUseCases.get_by_id(cmd, self.mock_bus, self.mock_container)

        self.assertEqual(result, self.user)
        self.mock_uow.user_repository.get_by_id.assert_called_once_with(
            self.user.id, with_permissions=True
        )

    def test_get_all_paginated_success(self):
        self.mock_uow.user_repository.count.return_value = 12
        self.mock_uow.user_repository.get_many.return_value = [self.user]

        cmd = GetAllUsersPaginatedCommand(current_page=2, limit=10)
        users, total, max_pages = UsersUseCases.get_all_paginated(
            cmd, self.mock_bus, self.mock_container
        )

        self.assertEqual(users, [self.user])
        self.assertEqual(total, 12)
        self.assertEqual(max_pages, 2)
        self.mock_uow.user_repository.get_many.assert_called_once_with(limit=10, offset=10)

    def test_get_all_paginated_invalid_page_raises_bad_request(self):
        cmd = GetAllUsersPaginatedCommand(current_page=0, limit=10)
        with pytest.raises(BadRequestException, match="Current page is invalid"):
            UsersUseCases.get_all_paginated(cmd, self.mock_bus, self.mock_container)

    def test_get_all_paginated_page_beyond_max_returns_empty_list(self):
        self.mock_uow.user_repository.count.return_value = 5
        cmd = GetAllUsersPaginatedCommand(current_page=3, limit=10)

        users, total, max_pages = UsersUseCases.get_all_paginated(
            cmd, self.mock_bus, self.mock_container
        )
        self.assertEqual(users, [])
        self.assertEqual(total, 5)
        self.assertEqual(max_pages, 1)

