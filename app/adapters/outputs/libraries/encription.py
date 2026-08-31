from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from app.domain.ports.libraries.abstract_encription import AbstractEncription


class Encription(AbstractEncription):
    _argon2_instance: PasswordHasher

    def __init__(self):
        self._argon2_instance = PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self._argon2_instance.hash(password)

    def verify_hash_password(self, password_hash: str, password: str) -> bool:
        try:
            return self._argon2_instance.verify(password_hash, password)
        except VerificationError:
            return False
