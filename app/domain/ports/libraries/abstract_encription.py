from abc import ABC, abstractmethod


class AbstractEncription(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError
