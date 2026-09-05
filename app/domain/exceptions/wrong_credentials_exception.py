from http import HTTPStatus

from app.domain.exceptions.base_http_exception import BaseHTTPException


class WrongCredentialsException(BaseHTTPException):
    def __init__(self):
        return super().__init__("Invalid phone or password", HTTPStatus.BAD_REQUEST)
