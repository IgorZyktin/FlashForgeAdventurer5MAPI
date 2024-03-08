"""Encoding and decoding machinery."""
import socket

from adventurer5m.api.commands_base import BaseCommand

BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 5


def execute(printer_ip, printer_port, command: BaseCommand) -> None:
    """Send command and receive response."""
    _socket = socket.socket()
    _socket.settimeout(TIMEOUT_SECONDS)
    _socket.connect((printer_ip, printer_port))
    _socket.send(command.code.encode())
    data = _socket.recv(BUFFER_SIZE)
    _socket.close()
    command.response = data.decode()
