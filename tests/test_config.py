import builtins
from logging import DEBUG, FATAL
import os
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from flask import Flask
import pytest

from app.config import Config


class TestConfig(unittest.TestCase):
    def test_config_development_environment(self):
        fake_local_settings = SimpleNamespace(
            postgresql_database_uri="user:pass@localhost:5432/db",
            flask_session_secret_key="super-secret",
        )
        with patch.dict(sys.modules, {"local_settings": fake_local_settings}):
            with patch.dict(os.environ, {"LOAD_INITIAL_DATABASES_DATA": "true"}):
                cfg = Config()

                self.assertFalse(cfg.is_production_environment)
                self.assertTrue(cfg.generate_initial_databases_data)
                self.assertEqual(cfg.postgresql_connection_uri, "user:pass@localhost:5432/db")

    def test_config_production_fallback_when_local_settings_missing(self):
        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "local_settings":
                raise ImportError("No module named local_settings")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fake_import):
            cfg = Config()

            self.assertTrue(cfg.is_production_environment)
            self.assertFalse(cfg.generate_initial_databases_data)

    @patch("app.config.basicConfig")
    def test_apply_to_logging_development(self, mock_basic_config):
        fake_local_settings = SimpleNamespace(
            postgresql_database_uri="user:pass@localhost:5432/db",
            flask_session_secret_key="super-secret",
        )
        with patch.dict(sys.modules, {"local_settings": fake_local_settings}):
            cfg = Config()
            cfg.apply_to_logging()

            mock_basic_config.assert_called_once_with(
                format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
                level=DEBUG,
            )

    @patch("app.config.basicConfig")
    def test_apply_to_logging_production(self, mock_basic_config):
        cfg = Config()
        cfg._environment = "production"
        cfg.apply_to_logging()

        mock_basic_config.assert_called_once_with(
            format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            filename="bikergroups_app.log",
            level=FATAL,
        )

    def test_apply_to_flask_app(self):
        fake_local_settings = SimpleNamespace(
            postgresql_database_uri="user:pass@localhost:5432/db",
            flask_session_secret_key="test-secret-key",
        )
        with patch.dict(sys.modules, {"local_settings": fake_local_settings}):
            cfg = Config()
            app = Flask(__name__)
            returned_app = cfg.apply_to_flask_app(app)

            self.assertIs(returned_app, app)
            self.assertEqual(app.config["SECRET_KEY"], "test-secret-key")
            self.assertEqual(app.config["MAX_CONTENT_LENGTH"], 16 * 1000 * 1000)


@pytest.mark.parametrize(
    "env_val,expected",
    [
        ("true", True),
        ("TRUE", True),
        ("false", False),
        ("", False),
    ],
)
def test_config_generate_initial_databases_data_env_parsing(env_val, expected):
    fake_local_settings = SimpleNamespace(
        postgresql_database_uri="user:pass@localhost:5432/db",
        flask_session_secret_key="secret",
    )
    with patch.dict(sys.modules, {"local_settings": fake_local_settings}):
        with patch.dict(os.environ, {"LOAD_INITIAL_DATABASES_DATA": env_val}):
            cfg = Config()
            assert cfg.generate_initial_databases_data is expected

