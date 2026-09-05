from http import HTTPStatus
from typing import Any


class BaseHTTPException(Exception):
    _status_code: HTTPStatus

    def __init__(
            self,
            error_message: str,
            status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(error_message)

        self._status_code = status_code

    @property
    def status_code(self) -> HTTPStatus:
        return self._status_code

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": str(self),
            "success": False,
        }
