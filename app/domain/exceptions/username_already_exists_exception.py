from http import HTTPStatus

from app.domain.exceptions.base_http_exception import BaseHTTPException


class UsernameAlreadyExistsException(BaseHTTPException):
    def __init__(self):
        return super().__init__("Username already exists", HTTPStatus.CONFLICT)
