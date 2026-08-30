from abc import ABC, abstractmethod

from app.domain.models.user_model import UserModel


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: UserModel) -> UserModel:
        raise NotImplementedError
