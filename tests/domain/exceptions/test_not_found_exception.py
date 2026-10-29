from http import HTTPStatus
import unittest

from app.domain.exceptions.not_found_exception import NotFoundException


class TestNotFoundException(unittest.TestCase):
    def test_not_found_exception_status_and_message(self):
        exc = NotFoundException("Resource not found")
        self.assertEqual(exc.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(
            exc.to_dict(),
            {"message": "Resource not found", "success": False},
        )

