import unittest
from unittest.mock import MagicMock
import pytest

from app.domain.ports.abstract_unit_of_work import AbstractUnitOfWork


class _DummyUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self._audit_log_repository = MagicMock()
        self._roadtrip_repository = MagicMock()
        self._user_permission_repository = MagicMock()
        self._user_repository = MagicMock()
        self.rolled_back = False

    def generate_initial_data(self) -> None:
        pass

    def rollback(self) -> None:
        self.rolled_back = True


class TestAbstractUnitOfWork(unittest.TestCase):
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            AbstractUnitOfWork()  # type: ignore

    def test_context_manager_and_repository_properties(self):
        uow = _DummyUnitOfWork()
        with uow as entered:
            self.assertIs(entered, uow)
            self.assertIsNotNone(uow.audit_log_repository)
            self.assertIsNotNone(uow.roadtrip_repository)
            self.assertIsNotNone(uow.user_permission_repository)
            self.assertIsNotNone(uow.user_repository)

        self.assertTrue(uow.rolled_back)

