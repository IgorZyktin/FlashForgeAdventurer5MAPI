"""Handlers for JSON-formatted responses."""
from flask import Blueprint

api = Blueprint('api', __name__)


@api.route('/')
def index():
    """Return current version of the app."""
    return {'version': '0.1'}
