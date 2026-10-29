import unittest
import pytest

from app.domain.ports.repositories.user_repository import UserRepository


class TestUserRepositoryPort(unittest.TestCase):
    def test_cannot_instantiate_user_repository_directly(self):
        with pytest.raises(TypeError):
            UserRepository()  # type: ignore

