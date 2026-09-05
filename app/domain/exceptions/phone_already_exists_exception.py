from http import HTTPStatus

from app.domain.exceptions.base_http_exception import BaseHTTPException


class PhoneAlreadyExistsException(BaseHTTPException):
    def __init__(self):
        return super().__init__("Phone already exists", HTTPStatus.CONFLICT)
