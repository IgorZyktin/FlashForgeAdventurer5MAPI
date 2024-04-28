"""Tests for parsing of printer responses."""
import unittest
from typing import Type

from adventurer5m import api


class AbstractTests:
    class BaseTestCase(unittest.TestCase):
        command_type: Type[api.commands_base.BaseCommand]

        @staticmethod
        def valid_input():
            return ''

        @staticmethod
        def valid_result():
            return {}

        def test_command_execution(self):
            # arrange
            command = self.command_type()
            command.response = self.valid_input()

            # act
            result = command.parse()

            # assert
            self.assertEqual(result, self.valid_result())


class TestProgress(AbstractTests.BaseTestCase):
    command_type = api.commands.Progress

    @staticmethod
    def valid_input():
        return (
            'CMD M27 Received.\r\n'
            'SD printing byte 98/100\r\n'
            'Layer: 163/166\r\n'
            'ok\r\n'
        )

    @staticmethod
    def valid_result():
        return {
            'byte_current': '98',
            'byte_target': '100',
            'layer_current': '163',
            'layer_target': '166',
        }


class TestTemperature(AbstractTests.BaseTestCase):
    command_type = api.commands.Temperature

    @staticmethod
    def valid_input():
        return (
            'CMD M105 Received.\r\n'
            'T0:239.9/240.0 T1:0.0/0.0 B:69.9/70.0\r\n'
            'ok\r\n'
        )

    @staticmethod
    def valid_result():
        return {
            'bed_t_current': '69.9',
            'bed_t_target': '70.0',
            't0_current': '239.9',
            't0_target': '240.0',
            't1_current': '0.0',
            't1_target': '0.0',
        }


class TestPosition(AbstractTests.BaseTestCase):
    command_type = api.commands.Position

    @staticmethod
    def valid_input():
        return (
            'CMD M114 Received.\r\n'
            'X:36.900 Y:7.760 Z:33.000 A:486.511 B:0\r\n'
            'ok\r\n'
        )

    @staticmethod
    def valid_result():
        return {
            'x_pos': '36.900',
            'y_pos': '7.760',
            'z_pos': '33.000',
            'a_pos': '486.511',
            'b_pos': '0',
        }


class TestInfo(AbstractTests.BaseTestCase):
    command_type = api.commands.Info

    @staticmethod
    def valid_input():
        return (
            'CMD M115 Received.\r\n'
            'Machine Type: Flashforge Adventurer 5M Pro\r\n'
            'Machine Name: Adventurer 5M Pro\r\n'
            'Firmware: v2.4.5\r\n'
            'SN: 12345\r\n'
            'X: 220 Y: 220 Z: 220\r\n'
            'Tool Count: 1\r\n'
            'Mac Address:00:00:00:00:00:00\r\n'
            'ok\r\n'
        )

    @staticmethod
    def valid_result():
        return {
            'machine_type': 'Flashforge Adventurer 5M Pro',
            'machine_name': 'Adventurer 5M Pro',
            'firmware': 'v2.4.5',
            'serial_number': '12345',
            'build_volume_x': '220',
            'build_volume_y': '220',
            'build_volume_z': '220',
            'tool_count': '1',
            'mac_address': '00:00:00:00:00:00',
        }


class TestStatus(AbstractTests.BaseTestCase):
    command_type = api.commands.Status

    @staticmethod
    def valid_input():
        return (
            'CMD M119 Received.\r\n'
            'Endstop: X-max: 110 Y-max: 110 Z-min: 0\r\n'
            'MachineStatus: BUILDING_COMPLETED\r\n'
            'MoveMode: PAUSED\r\n'
            'Status: S:1 L:0 J:0 F:0\r\n'
            'LED: 1\r\n'
            'CurrentFile: Portable Cable Winder - Large.gx\r\n'
            'ok\r\n'
        )

    @staticmethod
    def valid_result():
        return {
            'endstop_x_max': '110',
            'endstop_y_max': '110',
            'endstop_z_min': '0',
            'machine_status': 'BUILDING_COMPLETED',
            'move_mode': 'PAUSED',
            'status_s': '1',
            'status_l': '0',
            'status_j': '0',
            'status_f': '0',
            'led': '1',
            'current_file': 'Portable Cable Winder - Large.gx',
        }


if __name__ == '__main__':
    unittest.main()
