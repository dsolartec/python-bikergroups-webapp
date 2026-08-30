from flask import Flask

from src.adapters.http.views.ping_views import ping_views


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ping_views)

    return app
