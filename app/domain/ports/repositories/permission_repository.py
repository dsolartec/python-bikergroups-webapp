from abc import ABC, abstractmethod

from app.domain.models.permission_model import PermissionModel


class PermissionRepository(ABC):
    @abstractmethod
    def save(self, permission: PermissionModel) -> PermissionModel:
        raise NotImplementedError
