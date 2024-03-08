"""Handlers for human-readable responses."""
from flask import Blueprint

from adventurer5m import api

gui = Blueprint('gui', __name__)


@gui.route('/gui/<string:printer_ip>/<int:printer_port>')
def hello_world(printer_ip: str, printer_port: int):
    """Return something."""
    hello = api.commands.Temperature()
    api.transport.execute(
        printer_ip=printer_ip,
        printer_port=printer_port,
        command=hello,
    )
    print(hello.response)
    return "<p>Hello, World!</p>"
