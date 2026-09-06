from logging import DEBUG, FATAL, basicConfig
import os
from typing import Any, Literal

from flask import Flask


class Config:
    _environment: Literal['development'] | Literal['production']

    _postgresql_connection_uri: str
    _generate_initial_databases_data: bool

    _flask_session_secret_key: str

    def __init__(self):
        try:
            import local_settings

            self._environment = "development"

            self._postgresql_connection_uri = local_settings.postgresql_database_uri
            self._generate_initial_databases_data = (os.getenv("LOAD_INITIAL_DATABASES_DATA") or "false").lower() == "true"

            self._flask_session_secret_key = local_settings.flask_session_secret_key
        except:
            self._environment = "production"

            self._generate_initial_databases_data = False

    @property
    def is_production_environment(self) -> bool:
        return self._environment == "production"

    @property
    def generate_initial_databases_data(self) -> bool:
        return self._generate_initial_databases_data

    @property
    def postgresql_connection_uri(self) -> str:
        return self._postgresql_connection_uri

    def apply_to_logging(self):
        args: dict[str, Any] = {
            "format": "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
        }

        if self.is_production_environment:
            args["filename"] = "bikergroups_app.log"
            args["level"] = FATAL
        else:
            args["level"] = DEBUG

        basicConfig(**args)

    def apply_to_flask_app(self, app: Flask) -> Flask:
        app.config["SECRET_KEY"] = self._flask_session_secret_key
        app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000 # Max 16mb per file

        return app
