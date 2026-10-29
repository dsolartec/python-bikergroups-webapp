import unittest
import pytest

from app.domain.ports.libraries.abstract_encription import AbstractEncription


class TestAbstractEncription(unittest.TestCase):
    def test_cannot_instantiate_abstract_encription_directly(self):
        with pytest.raises(TypeError):
            AbstractEncription()  # type: ignore

