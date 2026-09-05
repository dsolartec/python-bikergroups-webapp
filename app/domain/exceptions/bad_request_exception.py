from http import HTTPStatus

from app.domain.exceptions.base_http_exception import BaseHTTPException


class BadRequestException(BaseHTTPException):
    def __init__(self, error_message: str):
        return super().__init__(error_message, HTTPStatus.BAD_REQUEST)
