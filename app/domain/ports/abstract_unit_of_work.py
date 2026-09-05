from abc import ABC, abstractmethod
from typing import Iterable

from app.domain.ports.repositories.audit_log_repository import AuditLogRepository
from app.domain.ports.repositories.roadtrip_repository import RoadTripRepository
from app.domain.ports.repositories.user_permission_repository import UserPermissionRepository
from app.domain.ports.repositories.user_repository import UserRepository


class AbstractUnitOfWork(ABC):
    _audit_log_repository: AuditLogRepository
    _roadtrip_repository: RoadTripRepository
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
    def audit_log_repository(self) -> AuditLogRepository:
        return self._audit_log_repository

    @property
    def roadtrip_repository(self) -> RoadTripRepository:
        return self._roadtrip_repository

    @property
    def user_permission_repository(self) -> UserPermissionRepository:
        return self._user_permission_repository

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository
