from http import HTTPStatus
from logging import basicConfig, getLogger

from flask import Flask, jsonify
from pydantic import ValidationError

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
    basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000 # Max 16mb per file
    app.url_map.strict_slashes = False

    app.register_blueprint(web_views)

    app.register_error_handler(Exception, error_middleware)

    return app
