"""Encoding and decoding machinery."""
import socket

from adventurer5m.api.commands_base import BaseCommand

BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 5
DEFAULT_PORT = 8899


def execute(printer_ip, printer_port, command: BaseCommand) -> None:
    """Send command and receive response."""
    _socket = socket.socket()
    _socket.settimeout(TIMEOUT_SECONDS)
    _socket.connect((printer_ip, printer_port))
    _socket.send(command.code.encode())

    chunks = []
    bytes_received = 0
    while True:
        chunk = _socket.recv(BUFFER_SIZE)

        if chunk:
            chunks.append(chunk)

        if len(chunk) < BUFFER_SIZE:
            break

        bytes_received += len(chunk)

    data = b''.join(chunks)

    _socket.close()
    command.response = data.decode()


def get_location(printer_address: str) -> tuple[str, int]:
    """Return printer IP and port."""
    if ':' in printer_address:
        pair = printer_address.split(':')
        printer_ip = pair[0]
        printer_port = int(pair[1])
    else:
        printer_ip = printer_address
        printer_port = DEFAULT_PORT

    return printer_ip, printer_port
