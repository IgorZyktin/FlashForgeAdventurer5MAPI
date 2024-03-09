"""Actual implementation of known commands."""

import re
from typing import Any

from adventurer5m.api.commands_base import BaseCommand, register


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

    byte_pattern = re.compile(
        r'SD printing byte (?P<byte_current>\d+)/(?P<byte_target>\d+)'
    )

    layer_pattern = re.compile(
        r'Layer: (?P<layer_current>\d+)/(?P<layer_target>\d+)'
    )

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}
        lines = self._pre_parse()

        bytes_re = self.byte_pattern.search(next(lines))
        result.update(bytes_re.groupdict())

        layer_re = self.layer_pattern.search(next(lines))
        result.update(layer_re.groupdict())

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

    pattern = re.compile(
        r'T0:\s*?(?P<t0_current>-?(\d+\.\d+|\d+))'
        r'/(?P<t0_target>-?(\d+\.\d+|\d+))\s*?'
        r'T1:\s*?-?(?P<t1_current>-?(\d+\.\d+|\d+))'
        r'/(?P<t1_target>-?(\d+\.\d+|\d+))\s*?'
        r'B:\s*?(?P<bed_t_current>-?(\d+\.\d+|\d+))'
        r'/(?P<bed_t_target>-?(\d+\.\d+|\d+))'
    )


@register
class Position(BaseCommand):
    """Send this to get info about print head coordinates.

    Expected response:
        CMD M114 Received.
        X:36.900 Y:7.760 Z:33.000 A:486.511 B:0
        ok
    """

    code = r'~M114\r\n'

    pattern = re.compile(
        r'X:\s*?(?P<x_pos>-?(\d+\.\d+|\d+))\s*?'
        r'Y:\s*?(?P<y_pos>-?(\d+\.\d+|\d+))\s*?'
        r'Z:\s*?(?P<z_pos>-?(\d+\.\d+|\d+))\s*?'
        r'A:\s*?(?P<a_pos>-?(\d+\.\d+|\d+))\s*?'
        r'B:\s*?(?P<b_pos>-?(\d+\.\d+|\d+))'
    )


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

    patterns = [
        re.compile(r'Machine Type:\s*?(?P<machine_type>.+)'),
        re.compile(r'Machine Name:\s*?(?P<machine_name>.+)'),
        re.compile(r'Firmware:\s*?(?P<firmware>.+)'),
        re.compile(r'SN:\s*?(?P<serial_number>.+)'),
        re.compile(
            r'X:\s*?(?P<build_volume_x>\d+) '
            r'Y:\s*?(?P<build_volume_y>\d+) '
            r'Z:\s*?(?P<build_volume_z>\d+)'
        ),
        re.compile(r'Tool Count:\s*?(?P<tool_count>.+)'),
        re.compile(r'Mac Address:\s*?(?P<mac_address>.+)'),
    ]

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}

        for line, pattern in zip(self._pre_parse(), self.patterns):
            regex_results = pattern.search(line)
            result.update(regex_results.groupdict())

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

    patterns = [
        re.compile(
            r'Endstop: X-max:\s*?(?P<endstop_x_max>\d+) '
            r'Y-max:\s*?(?P<endstop_y_max>\d+) '
            r'Z-min:\s*?(?P<endstop_z_min>\d+)'
        ),
        re.compile(r'MachineStatus: (?P<machine_status>.+)'),
        re.compile(r'MoveMode: (?P<move_mode>.+)'),
        re.compile(
            r'Status: S:\s*?(?P<status_s>\d+) '
            r'L:\s*?(?P<status_l>\d+) '
            r'J:\s*?(?P<status_j>\d+) '
            r'F:\s*?(?P<status_f>\d+)'
        ),
        re.compile(r'LED: (?P<led>.+)'),
        re.compile(r'CurrentFile:\s?(?P<current_file>.*)'),

    ]

    def parse(self) -> dict[str, Any]:
        """Process response and return result as JSON."""
        result: dict[str, Any] = {}

        for line, pattern in zip(self._pre_parse(), self.patterns):
            regex_results = pattern.search(line)
            result.update(regex_results.groupdict())

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
        return {'message': next(self._pre_parse())}
