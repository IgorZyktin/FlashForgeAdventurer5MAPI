"""Base command machinery."""

import abc
import logging
import re
from typing import Type, Any, Iterator, Pattern

from adventurer5m import exceptions

LOG = logging.getLogger(__name__)


class BaseCommand(abc.ABC):
    """Base class for all commands."""

    code: str
    pattern: Pattern = re.compile(r'.*')
    response: str = ''

    def _pre_parse(self) -> Iterator[str]:
        """Prepare response for parsing."""
        LOG.info(
            'Got response: \n%(spacer)s\n%(response)s%(spacer)s',
            {
                'spacer': '-' * 70,
                'response': self.response,
            },
        )

        try:
            head, *body, tail = self.response.strip().splitlines()
        except Exception as exc:
            message = (
                f'Got response in unusual format: {exc}, {self.response!r}'
            )
            LOG.exception(message)
            raise exceptions.UnexpectedResponse(message)

        if tail != 'ok':
            message = f'Result not ends with ok: {self.response!r}'
            raise exceptions.UnexpectedResponse(message)

        for line in body:
            yield line.strip()

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}
        lines = self._pre_parse()

        regex_results = self.pattern.search(next(lines))
        result.update(regex_results.groupdict())

        return result


_commands: dict[str, Type[BaseCommand]] = {}


def register(command: Type[BaseCommand]) -> Type[BaseCommand]:
    """Save command to the storage."""
    _commands[command.__name__.casefold()] = command
    return command


def get_command(name: str) -> Type[BaseCommand] | None:
    """Return command type or None."""
    return _commands.get(name.casefold())
