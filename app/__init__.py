from http import HTTPStatus

from flask import Flask, jsonify

from app.adapters.inputs.apis.auth_views import auth_views
from app.adapters.inputs.apis.ping_views import ping_views
from app.domain.exceptions.base_http_exception import BaseHTTPException


def error_middleware(e: Exception):
    if isinstance(e, BaseHTTPException):
        return jsonify(e.to_dict()), e.status_code

    return jsonify({
        "message": "Internal server error",
        "success": False,
    }), HTTPStatus.INTERNAL_SERVER_ERROR

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.register_blueprint(ping_views)
    app.register_blueprint(auth_views)

    app.register_error_handler(Exception, error_middleware)

    return app
