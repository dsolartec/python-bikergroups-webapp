from functools import wraps
from typing import Any, Callable

from flask import g, redirect

from app.domain.enums.permission_enum import PermissionEnum
from app.domain.models.user_model import UserModel


def require_permissions(permissions: list[PermissionEnum], redirect_to: str = "/") -> Callable[[Any], Any]:
    def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            user: UserModel | None = g.user
            if user is None:
                return redirect(redirect_to)

            if len(permissions) == 0:
                return fn(*args, **kwargs)

            user_permissions_names = [permission.name for permission in user.permissions]

            for permission_name in set(permissions):
                if permission_name in user_permissions_names:
                    return fn(*args, **kwargs)

            return redirect(redirect_to)

        return inner

    return wrapper
