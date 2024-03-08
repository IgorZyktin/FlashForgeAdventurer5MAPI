"""Application entry point."""
from flask import Flask

from adventurer5m.api import api
from adventurer5m.gui import gui


def create_app() -> Flask:
    """Create instance of the application."""
    _app = Flask(__name__)
    _app.register_blueprint(api.api)
    _app.register_blueprint(gui.gui)
    return _app


app = create_app()
