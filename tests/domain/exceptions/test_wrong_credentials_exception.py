from http import HTTPStatus
import unittest

from app.domain.exceptions.wrong_credentials_exception import WrongCredentialsException


class TestWrongCredentialsException(unittest.TestCase):
    def test_wrong_credentials_exception(self):
        exc = WrongCredentialsException()
        self.assertEqual(exc.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            exc.to_dict(),
            {"message": "Invalid phone or password", "success": False},
        )

