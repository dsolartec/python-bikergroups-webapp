from http import HTTPStatus
import unittest

from app.domain.exceptions.phone_already_exists_exception import PhoneAlreadyExistsException


class TestPhoneAlreadyExistsException(unittest.TestCase):
    def test_phone_already_exists_exception(self):
        exc = PhoneAlreadyExistsException()
        self.assertEqual(exc.status_code, HTTPStatus.CONFLICT)
        self.assertEqual(
            exc.to_dict(),
            {"message": "Phone already exists", "success": False},
        )

