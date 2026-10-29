from http import HTTPStatus
import unittest

from app.domain.exceptions.bad_request_exception import BadRequestException


class TestBadRequestException(unittest.TestCase):
    def test_bad_request_exception_status_and_message(self):
        exc = BadRequestException("Invalid parameter")
        self.assertEqual(exc.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            exc.to_dict(),
            {"message": "Invalid parameter", "success": False},
        )

