from http import HTTPStatus
from logging import getLogger

from flask import Flask, jsonify
from pydantic import ValidationError

from app.adapters.container import Container
from app.adapters.inputs.web_views import web_views
from app.domain.exceptions.base_http_exception import BaseHTTPException


_logger = getLogger(__name__)


def error_middleware(e: Exception):
    if isinstance(e, BaseHTTPException):
        return jsonify(e.to_dict()), e.status_code

    if isinstance(e, ValidationError):
        return jsonify({
            "validations": [
                {
                    "field": ", ".join(error["loc"]),
                    "message": error["msg"],
                }
                for error in e.errors()
            ]
        }), HTTPStatus.BAD_REQUEST

    _logger.error("Invalid exception: %s", str(e))

    return jsonify({
        "message": "Internal server error",
        "success": False,
    }), HTTPStatus.INTERNAL_SERVER_ERROR


def create_app():
    container = Container()

    config = container.config()
    config.apply_to_logging()

    if config.generate_initial_databases_data:
        with container.unit_of_work() as uow:
            uow.generate_initial_data()

    app = config.apply_to_flask_app(Flask(__name__))    
    app.url_map.strict_slashes = False

    app.register_error_handler(Exception, error_middleware)
    app.register_blueprint(web_views)

    return app
