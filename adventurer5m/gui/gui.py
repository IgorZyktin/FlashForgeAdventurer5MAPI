"""Handlers for human-readable responses."""
from flask import Blueprint

gui = Blueprint('gui', __name__)


@gui.route('/gui')
def hello_world():
    """Return something."""
    return "<p>Hello, World!</p>"
