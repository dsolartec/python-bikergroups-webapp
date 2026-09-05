from http import HTTPStatus

from flask import Flask, jsonify
from pydantic import ValidationError

from app.adapters.inputs.apis.auth_views import auth_views
from app.adapters.inputs.apis.ping_views import ping_views
from app.adapters.inputs.apis.roadtrip_views import roadtrip_views
from app.domain.exceptions.base_http_exception import BaseHTTPException


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

    return jsonify({
        "message": "Internal server error",
        "success": False,
    }), HTTPStatus.INTERNAL_SERVER_ERROR

def create_app():
    app = Flask(__name__)

    app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000 # Max 16mb per file
    app.url_map.strict_slashes = False

    app.register_blueprint(ping_views)
    app.register_blueprint(auth_views)
    app.register_blueprint(roadtrip_views)

    app.register_error_handler(Exception, error_middleware)

    return app
