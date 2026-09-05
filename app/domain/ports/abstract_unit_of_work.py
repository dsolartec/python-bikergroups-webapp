from abc import ABC, abstractmethod
from typing import Iterable

from app.domain.ports.repositories.user_permission_repository import UserPermissionRepository
from app.domain.ports.repositories.user_repository import UserRepository


class AbstractUnitOfWork(ABC):
    _user_permission_repository: UserPermissionRepository
    _user_repository: UserRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def expose_data(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def refresh(self, instance: object, attribute_names: Iterable[str] | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    def __exit__(self, *args):
        self.rollback()

    @property
    def user_permission_repository(self) -> UserPermissionRepository:
        return self._user_permission_repository

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository
