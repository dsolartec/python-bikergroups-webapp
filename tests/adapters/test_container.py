import unittest
from unittest.mock import patch

from app.adapters.container import Container
from app.adapters.outputs.libraries.encription import Encription
from app.config import Config


class TestContainer(unittest.TestCase):
    def test_container_provides_config_singleton(self):
        container = Container()
        cfg1 = container.config()
        cfg2 = container.config()

        self.assertIsInstance(cfg1, Config)
        self.assertIs(cfg1, cfg2)

    def test_container_provides_encription_factory(self):
        container = Container()
        enc1 = container.encription()
        enc2 = container.encription()

        self.assertIsInstance(enc1, Encription)
        self.assertIsNot(enc1, enc2)

    @patch("app.adapters.outputs.datasources.unit_of_work.create_engine")
    @patch("app.adapters.outputs.datasources.unit_of_work.scoped_session")
    @patch("app.adapters.outputs.datasources.unit_of_work.sessionmaker")
    def test_container_provides_unit_of_work(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        container = Container()
        uow = container.unit_of_work()

        self.assertIsNotNone(uow)
        mock_create_engine.assert_called_once()

