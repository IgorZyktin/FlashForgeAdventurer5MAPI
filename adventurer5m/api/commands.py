"""Actual implementation of known commands."""
import re
from typing import Any

from adventurer5m.api.commands_base import BaseCommand, register

NamedNumber = re.compile(
    r"""
    ([\w-]+)           # one or more letters
    :               # semicolon
    \s*?            # optional space
    (\d+\.\d+|\d+)  # one or more digits, possibly float
    """,
    flags=re.VERBOSE,
)

NamedDelta = re.compile(
    r"""
    (\w+\d*?)       # one or more letters followed by zero or more digits
    :               # semicolon
    \s*?            # optional space
    (\d+\.\d+|\d+)  # one or more digits, possibly float
    /               # literal slash
    (\d+\.\d+|\d+)  # one or more digits, possibly float
    """,
    flags=re.VERBOSE,
)

NamedProgress = re.compile(
    r"""
    (\w+)  # one or more letters
    :?     # optional semicolon
    \s*?   # optional space
    (\d+)  # one or more digits, possibly float
    /      # literal slash
    (\d+)  # one or more digits
    """,
    flags=re.VERBOSE,
)


@register
class Progress(BaseCommand):
    """Send this to get info about print progress.

    Expected response:
        CMD M27 Received.
        SD printing byte 98/100
        Layer: 163/166
        ok
    """
    code = r'~M27\r\n'

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}

        for line in self._pre_parse():
            for each in NamedProgress.finditer(line):
                category, current, target = each.groups()
                result[category.strip()] = {
                    'current': int(current),
                    'target': int(target),
                }

        return result


@register
class Temperature(BaseCommand):
    """Send this to get info about temperature.

    Expected response:
        CMD M105 Received.
        T0:239.9/240.0 T1:0.0/0.0 B:69.9/70.0
        ok
    """
    code = r'~M105\r\n'

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}

        line = next(self._pre_parse())
        for each in NamedDelta.finditer(line):
            category, current, target = each.groups()
            if category.casefold() == 'B'.casefold():
                category = 'Bed'

            result[category.strip()] = {
                'current': float(current),
                'target': float(target),
            }

        return result


@register
class Position(BaseCommand):
    """Send this to get info about print head coordinates.

    Expected response:
        CMD M114 Received.
        X:36.900 Y:7.760 Z:33.000 A:486.511 B:0
        ok
    """
    code = r'~M114\r\n'

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}

        line = next(self._pre_parse())
        for each in NamedNumber.finditer(line):
            key, value = each.groups()
            result[key.strip()] = float(value)

        return result


@register
class Info(BaseCommand):
    """Send this to get info about the printer.

    Expected response:
        CMD M115 Received.
        Machine Type: Flashforge Adventurer 5M Pro
        Machine Name: Adventurer 5M Pro
        Firmware: v2.4.5
        SN: 12345
        X: 220 Y: 220 Z: 220
        Tool Count: 1
        Mac Address:00:00:00:00:00:00
        ok
    """
    code = r'~M115\r\n'

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}

        for line in self._pre_parse():
            total = line.count(':')

            if total == 3:
                for each in NamedNumber.finditer(line):
                    key, value = each.groups()
                    result[key.strip() + '-zone'] = float(value.strip())
            else:
                key, value = line.split(':', maxsplit=1)
                result[key.strip()] = value.strip()

        return result


@register
class Status(BaseCommand):
    """Send this to get status of the printer.

    Expected response:
        CMD M119 Received.
        Endstop: X-max: 110 Y-max: 110 Z-min: 0
        MachineStatus: BUILDING_COMPLETED
        MoveMode: PAUSED
        Status: S:1 L:0 J:0 F:0
        LED: 1
        CurrentFile: Portable Cable Winder - Large.gx
        ok
    """
    code = r'~M119\r\n'

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}

        for line in self._pre_parse():
            total = line.count(':')
            key, value = line.split(':', maxsplit=1)

            if total == 1:
                result[key.strip()] = value.strip()

            else:
                category = {}
                for each in NamedNumber.finditer(value):
                    sub_key, value = each.groups()
                    category[sub_key.strip()] = int(value.strip())

                result[key.strip()] = category

        return result


@register
class Hello(BaseCommand):
    """Send this to start interaction with the printer.

    Expected response:
        CMD M601 Received.
        Control Success V2.1.
        ok
    """
    code = r'~M601 S1\r\n'

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        return {'response': next(self._pre_parse())}
