from abc import ABC, abstractmethod

from app.domain.models.access_token_model import AccessTokenModel
from app.domain.models.refresh_token_model import RefreshTokenModel


class AbstractAuthenticator(ABC):
    @abstractmethod
    def generate_access_token(self, permissions_names: list[str], user_id: str, phone: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_refresh_token(self, user_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_access_token(self, token_string: str, do_time_check: bool = True) -> AccessTokenModel:
        raise NotImplementedError

    @abstractmethod
    def parse_refresh_token(self, token_string: str, do_time_check: bool = True) -> RefreshTokenModel:
        raise NotImplementedError
