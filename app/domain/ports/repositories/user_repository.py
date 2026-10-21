from abc import ABC, abstractmethod

from app.domain.models.user_model import UserModel


class UserRepository(ABC):
    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: str, with_permissions: bool = False) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    def get_by_phone(self, phone: str, with_permissions: bool = False) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    def get_many(self, limit: int, offset: int) -> list[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def save(self, user: UserModel) -> UserModel:
        raise NotImplementedError
