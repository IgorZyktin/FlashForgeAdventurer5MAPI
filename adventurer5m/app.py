"""Application entry point."""
import logging

from flask import Flask

from adventurer5m import api
from adventurer5m import gui


def create_app() -> Flask:
    """Create instance of the application."""
    logging.basicConfig(
        format='%(asctime)s - %(levelname)7s - %(message)s',
        level=logging.INFO,
    )

    _app = Flask(__name__)
    _app.register_blueprint(api.api.api)
    _app.register_blueprint(gui.gui.gui)

    return _app


app = create_app()
