from abc import ABC, abstractmethod

from app.domain.models.user_permission_model import UserPermissionModel


class UserPermissionRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> list[UserPermissionModel]:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: UserPermissionModel) -> bool:
        raise NotImplementedError
