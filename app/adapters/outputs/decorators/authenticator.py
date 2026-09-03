from functools import wraps
from typing import Any, Callable

from flask import request
from jwt.exceptions import JWTDecodeError

from app.adapters.container import Container
from app.domain.exceptions.unauthorized_exception import UnauthorizedException


def authenticator(
        permission_names: list[str],
        do_time_check: bool = True,
) -> Callable[[Any], Any]:
    authenticator = Container().authenticator()

    def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            token_string = request.headers.get("Authorization")
            if token_string is None or not token_string.startswith("Bearer "):
                raise UnauthorizedException("Invalid access token")

            try:
                access_token = authenticator.parse_access_token(
                    token_string.replace("Bearer ", "", 1),
                    do_time_check=do_time_check,
                )
            except JWTDecodeError as de:
                raise UnauthorizedException(str(de)) from de

            if len(permission_names) == 0:
                return fn(*args, **kwargs)

            for permission_name in set(permission_names):
                if permission_name in access_token.permissions_names:
                    return fn(*args, **kwargs)

            raise UnauthorizedException("User doesn't have permission")

        return inner

    return wrapper
