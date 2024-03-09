"""Handlers for human-readable responses."""

from flask import Blueprint, render_template

from adventurer5m import api as api_module

gui = Blueprint('gui', __name__)


@gui.route('/<string:language>/<string:printer_address>')
def graphical_user_interface(language: str, printer_address: str):
    """Render human-readable HTML page."""
    printer_ip, printer_port = api_module.transport.get_location(
        printer_address=printer_address,
    )

    return render_template(
        f'index_ru.html' if language.lower() == 'ru' else 'index_en.html',
        printer_address=f'{printer_ip}:{printer_port}',
        printer_ip=printer_ip,
        printer_port=printer_port,
    )
