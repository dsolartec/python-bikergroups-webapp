import unittest

from app.adapters.outputs.libraries.encription import Encription


class TestEncription(unittest.TestCase):
    def setUp(self):
        self.encription = Encription()

    def test_hash_and_verify_password_success(self):
        raw_password = "MySecurePassword123"
        hashed = self.encription.hash_password(raw_password)

        self.assertNotEqual(hashed, raw_password)
        self.assertTrue(self.encription.verify_hash_password(hashed, raw_password))

    def test_verify_hash_password_returns_false_for_wrong_password(self):
        hashed = self.encription.hash_password("CorrectPassword123")
        self.assertFalse(self.encription.verify_hash_password(hashed, "WrongPassword123"))

