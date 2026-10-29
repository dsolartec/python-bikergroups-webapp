from http import HTTPStatus
import unittest
from unittest.mock import MagicMock, patch

from flask import Flask
from pydantic import BaseModel, ValidationError
import pytest

from app import create_app, error_middleware
from app.domain.exceptions.bad_request_exception import BadRequestException


class _DummyModel(BaseModel):
    age: int


class TestAppInit(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_error_middleware_handles_base_http_exception(self):
        with self.app.app_context():
            exc = BadRequestException("Invalid input")
            response, status_code = error_middleware(exc)

            self.assertEqual(status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(
                response.get_json(),
                {"message": "Invalid input", "success": False},
            )

    def test_error_middleware_handles_pydantic_validation_error(self):
        with self.app.app_context():
            try:
                _DummyModel(age="not-an-int")
            except ValidationError as exc:
                response, status_code = error_middleware(exc)

                self.assertEqual(status_code, HTTPStatus.BAD_REQUEST)
                data = response.get_json()
                self.assertIn("validations", data)
                self.assertEqual(data["validations"][0]["field"], "age")

    def test_error_middleware_handles_unexpected_exception(self):
        with self.app.app_context():
            exc = RuntimeError("Unexpected crash")
            response, status_code = error_middleware(exc)

            self.assertEqual(status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
            self.assertEqual(
                response.get_json(),
                {"message": "Internal server error", "success": False},
            )

    @patch("app.Container")
    def test_create_app_without_initial_data(self, mock_container_cls):
        mock_container = MagicMock()
        mock_config = MagicMock()
        mock_config.generate_initial_databases_data = False
        mock_config.apply_to_flask_app.side_effect = lambda app: app
        mock_container.config.return_value = mock_config
        mock_container_cls.return_value = mock_container

        app = create_app()

        self.assertIsInstance(app, Flask)
        self.assertFalse(app.url_map.strict_slashes)
        mock_config.apply_to_logging.assert_called_once()
        mock_config.apply_to_flask_app.assert_called_once()
        mock_container.unit_of_work.assert_not_called()

    @patch("app.Container")
    def test_create_app_with_initial_data(self, mock_container_cls):
        mock_container = MagicMock()
        mock_config = MagicMock()
        mock_config.generate_initial_databases_data = True
        mock_config.apply_to_flask_app.side_effect = lambda app: app
        mock_container.config.return_value = mock_config

        mock_uow = MagicMock()
        mock_uow.__enter__.return_value = mock_uow
        mock_container.unit_of_work.return_value = mock_uow
        mock_container_cls.return_value = mock_container

        app = create_app()

        self.assertIsInstance(app, Flask)
        mock_uow.generate_initial_data.assert_called_once()


@pytest.mark.parametrize("generate_data", [False, True])
def test_create_app_registers_blueprints(generate_data):
    with patch("app.Container") as mock_container_cls:
        mock_container = MagicMock()
        mock_config = MagicMock()
        mock_config.generate_initial_databases_data = generate_data
        mock_config.apply_to_flask_app.side_effect = lambda app: app
        mock_container.config.return_value = mock_config
        mock_uow = MagicMock()
        mock_uow.__enter__.return_value = mock_uow
        mock_container.unit_of_work.return_value = mock_uow
        mock_container_cls.return_value = mock_container

        app = create_app()
        assert "web_views" in app.blueprints
        assert "admin_views" in app.blueprints

