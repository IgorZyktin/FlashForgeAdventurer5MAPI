"""Handlers for JSON-formatted responses."""
import json
from http import HTTPStatus

from flask import Blueprint, Response
from flask import abort

from adventurer5m import api as api_module
from adventurer5m import exceptions

api = Blueprint('api', __name__)

DEFAULT_PORT = 8899


class JsonResponse(Response):
    """JSON-specific response."""
    default_mimetype: str = 'application/json'


@api.route('/')
def index():
    """Return current version of the app."""
    return {'version': '0.1'}


@api.route('/api/execute/<string:printer_address>/<string:command_name>')
def execute_command(printer_address: str, command_name: str):
    """Ask printer and return result of the command."""
    if ':' in printer_address:
        pair = printer_address.split(':')
        printer_ip = pair[0]
        printer_port = int(pair[1])
    else:
        printer_ip = printer_address
        printer_port = DEFAULT_PORT

    command_type = api_module.commands_base.get_command(command_name)

    if command_type is None:
        payload = {'error': f'Unknown command {command_name!r}'}
        abort(
            JsonResponse(
                response=json.dumps(payload, ensure_ascii=False),
                status=HTTPStatus.NOT_FOUND,
            ),
        )

    command = command_type()

    try:
        api_module.transport.execute(
            printer_ip=printer_ip,
            printer_port=printer_port,
            command=command,
        )
    except exceptions.GeneralException as exc:
        payload = {'error': str(exc)}
        abort(
            JsonResponse(
                response=json.dumps(payload, ensure_ascii=False),
                status=HTTPStatus.NOT_FOUND,
            ),
        )

    return command.parse()
