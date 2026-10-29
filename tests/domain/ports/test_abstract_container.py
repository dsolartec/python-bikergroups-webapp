import unittest

from app.domain.ports.abstract_container import AbstractContainer


class TestAbstractContainer(unittest.TestCase):
    def test_abstract_container_annotations(self):
        annotations = AbstractContainer.__annotations__
        self.assertIn("config", annotations)
        self.assertIn("unit_of_work", annotations)
        self.assertIn("encription", annotations)

