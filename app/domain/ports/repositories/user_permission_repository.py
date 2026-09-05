from abc import ABC, abstractmethod

from app.domain.models.user_permission_model import UserPermissionModel


class UserPermissionRepository(ABC):
    @abstractmethod
    def save(self, data: UserPermissionModel) -> bool:
        raise NotImplementedError
