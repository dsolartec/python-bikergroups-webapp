import unittest
import pytest

from app.domain.ports.repositories.user_permission_repository import UserPermissionRepository


class TestUserPermissionRepositoryPort(unittest.TestCase):
    def test_cannot_instantiate_user_permission_repository_directly(self):
        with pytest.raises(TypeError):
            UserPermissionRepository()  # type: ignore

