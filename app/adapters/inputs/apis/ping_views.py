from http import HTTPStatus

from flask import Blueprint


ping_views = Blueprint("ping_views", __name__)


@ping_views.get("/ping")
def ping():
    return "pong", HTTPStatus.OK
