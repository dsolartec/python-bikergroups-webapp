from abc import ABC, abstractmethod

from app.domain.models.user_model import UserModel


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    def save(self, user: UserModel) -> UserModel:
        raise NotImplementedError
