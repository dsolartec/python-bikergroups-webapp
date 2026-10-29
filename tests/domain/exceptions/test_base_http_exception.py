from http import HTTPStatus
import unittest

from app.domain.exceptions.base_http_exception import BaseHTTPException


class TestBaseHTTPException(unittest.TestCase):
    def test_default_status_code_and_to_dict(self):
        exc = BaseHTTPException("Something went wrong")
        self.assertEqual(exc.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(
            exc.to_dict(),
            {"message": "Something went wrong", "success": False},
        )

    def test_custom_status_code(self):
        exc = BaseHTTPException("Forbidden action", HTTPStatus.FORBIDDEN)
        self.assertEqual(exc.status_code, HTTPStatus.FORBIDDEN)

