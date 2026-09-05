from functools import wraps
from typing import Any, Callable

from flask import request
from jwt.exceptions import JWTDecodeError

from app.adapters.container import Container
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.unauthorized_exception import UnauthorizedException


def authenticator(
        permissions: list[PermissionEnum],
        do_time_check: bool = True,
) -> Callable[[Any], Any]:
    container = Container()
    authenticator = container.authenticator()

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

                with container.unit_of_work() as uow:
                    try:
                        uow.user_repository.get_by_id(access_token.user_id)
                    except NotFoundException:
                        raise UnauthorizedException("Invalid access token")

                kwargs["logged_access_token"] = access_token
            except JWTDecodeError as de:
                raise UnauthorizedException(str(de)) from de

            if len(permissions) == 0:
                return fn(*args, **kwargs)

            for permission_name in set(permissions):
                if permission_name.value in access_token.permissions_names:
                    return fn(*args, **kwargs)

            raise UnauthorizedException("User cannot perform this action")

        return inner

    return wrapper
