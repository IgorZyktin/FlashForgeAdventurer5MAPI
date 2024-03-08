"""Base command machinery."""
import abc
import logging
from typing import Type, Any, Iterator

from adventurer5m import exceptions

LOG = logging.getLogger(__name__)


class BaseCommand(abc.ABC):
    """Base class for all commands."""
    code: str
    response: str = ''

    def _pre_parse(self) -> Iterator[str]:
        """Prepare response for parsing."""
        LOG.info(
            'Got response: \n%(spacer)s\n%(response)s%(spacer)s',
            {
                'spacer': '-' * 70,
                'response': self.response,
            }
        )

        head, *body, tail = self.response.strip().splitlines()

        if tail != 'ok':
            message = f'Result not ends with ok: {self.response!r}'
            raise exceptions.UnexpectedResponse(message)

        for line in body:
            yield line.strip()

    @abc.abstractmethod
    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""


_commands: dict[str, Type[BaseCommand]] = {}


def register(command: Type[BaseCommand]) -> Type[BaseCommand]:
    """Save command to the storage."""
    _commands[command.__name__.casefold()] = command
    return command


def get_command(name: str) -> Type[BaseCommand] | None:
    """Return command type or None."""
    return _commands.get(name.casefold())
