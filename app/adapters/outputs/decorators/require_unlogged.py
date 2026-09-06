from functools import wraps
from typing import Any, Callable

from flask import g, redirect

from app.domain.models.user_model import UserModel


def require_unlogged(redirect_to: str = "/") -> Callable[[Any], Any]:
    def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            user: UserModel | None = g.user
            if user is None:
                return fn(*args, **kwargs)

            return redirect(redirect_to)

        return inner

    return wrapper
