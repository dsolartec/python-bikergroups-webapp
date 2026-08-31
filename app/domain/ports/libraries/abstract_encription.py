from abc import ABC, abstractmethod


class AbstractEncription(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_hash_password(self, password_hash: str, password: str) -> bool:
        raise NotImplementedError
