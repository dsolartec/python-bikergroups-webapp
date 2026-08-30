from argon2 import PasswordHasher

from app.domain.ports.libraries.abstract_encription import AbstractEncription


class Encription(AbstractEncription):
    _argon2_instance: PasswordHasher

    def __init__(self):
        self._argon2_instance = PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self._argon2_instance.hash(password)
