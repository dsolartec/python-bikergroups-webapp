import base64
from datetime import datetime, timedelta, timezone

from jwt import AbstractJWKBase, JWT, jwk_from_dict
from jwt.utils import get_int_from_datetime

from app.domain.models.access_token_model import AccessTokenModel
from app.domain.models.refresh_token_model import RefreshTokenModel
from app.domain.ports.libraries.abstract_authenticator import AbstractAuthenticator


class Authenticator(AbstractAuthenticator):
    _jwt: JWT
    _access_token_signing_key: AbstractJWKBase
    _refresh_token_signing_key: AbstractJWKBase

    def __init__(self, access_token_secret_key: str, refresh_token_secret_key: str):
        self._jwt = JWT()
        self._access_token_signing_key = jwk_from_dict({
            "kty": "oct",
            "k": base64.b64encode(access_token_secret_key.encode()).decode(),
        })
        self._refresh_token_signing_key = jwk_from_dict({
            "kty": "oct",
            "k": base64.b64encode(refresh_token_secret_key.encode()).decode(),
        })

    def generate_access_token(
            self,
            permissions_names: list[str],
            user_id: str,
            username: str,
    ) -> str:
        return self._jwt.encode(AccessTokenModel(
            expiration_timestamp=get_int_from_datetime(datetime.now(timezone.utc) + timedelta(hours=8)),
            generation_timestamp=get_int_from_datetime(datetime.now(timezone.utc)),
            permissions_names=permissions_names,
            user_id=user_id,
            username=username,
        ).model_dump(), self._access_token_signing_key)
 
    def generate_refresh_token(self, user_id: str) -> str:
        return self._jwt.encode(RefreshTokenModel(
            expiration_timestamp=get_int_from_datetime(datetime.now(timezone.utc) + timedelta(days=30)),
            generation_timestamp=get_int_from_datetime(datetime.now(timezone.utc)),
            user_id=user_id,
        ).model_dump(), self._refresh_token_signing_key)

    def parse_access_token(
            self,
            token_string: str,
            do_time_check: bool = True,
    ) -> AccessTokenModel:
        return AccessTokenModel.model_validate(self._jwt.decode(
            token_string,
            self._access_token_signing_key,
            do_time_check=do_time_check,
        ))

    def parse_refresh_token(
            self,
            token_string: str,
            do_time_check: bool = True,
    ) -> RefreshTokenModel:
        return RefreshTokenModel.model_validate(self._jwt.decode(
            token_string,
            self._refresh_token_signing_key,
            do_time_check=do_time_check,
        ))
