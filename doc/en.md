# Documentation

Known and tested printer codes:

| Code         | Action                         |
|--------------|--------------------------------|
| ~M27\r\n     | Get progress info              |
| ~M105\r\n    | Get temperature info           |
| ~M114\r\n    | Get position info              |
| ~M115\r\n    | Get info about the printer     |
| ~M119\r\n    | Get status of the printer      |
| ~M601 S1\r\n | Initial message to get control |

Untested codes:

| Code                     | Action             |
|--------------------------|--------------------|
| ~M23\r\n                 | Print from SD?     |
| ~M24\r\n                 | Resume?            |
| ~M25\r\n                 | Pause?             |
| ~M26\r\n                 | Stop?              |
| ~M28\r\n                 | Save on SD?        |
| ~M29\r\n                 | Stop saving on SD? |
| ~G28\r\n                 | Home?              |
| ~M146 r255 g255 b255\r\n | Light on?          |
| ~M146 r0 g0 b0\r\n       | Light off?         |
| ~M148\r\n                | Sound?             |
| ~M650\r\n                | Calibration?       |

```
To print from file: 'M650', 'M28 <file size> 0:/user/<file name>', encode the file with base64 and then send 4096 bytes each time, 'M29', 'M23 0:/user/<file name>'

Max length for file name is 36 bytes. File size is the base64 encoded size.

Update; To send a file with TCP socket to Finder: Do not encode with base64, still send 4096 bytes at a time but add 16 bytes at the start. The first four bytes should be 0x5a, 0x5a, 0xa5, 0xa5. Next four bytes should be a four byte unsigned big endian counter starting at 0. Next four bytes should be a four byte unsigned big endian data length (4096, except last packet). The last four bytes should be a big endian CRC32 of the data for that packet. The last packet has to be padded with 0x00 until the data length is 4096 bytes. The CRC is for the data without padding.

To connect through USB I used pyusb (https://github.com/pyusb/pyusb). Search for the printer with vendor '0x2b71' and product '0x0002'. You can send commands to endpoint 0x1 and read response from endpoint 0x81. To send a file you use endpoint 0x3.
```

## Install

To install this you need `docker`.

Build and run:

```shell
git clone https://github.com/IgorZyktin/FlashForgeAdventurer5MAPI.git
cd FlashForgeAdventurer5MAPI
docker build -t flashforge:v0.2 .
docker run -d -p 9876:9876 flashforge:v0.2
```

GUI is located at:

```shell
http://127.0.0.1:9876/en/<ip address of the printer>
```

## Manual requests

If you want to, you can request the API manually.

Please note that the application passes API responses without modification, you
will get string values formatted as they initially were received.

```shell
PORT=9876
PRINTER_IP=192.168.1.45
```

```shell
curl http://127.0.0.1:${PORT}/api/execute/${PRINTER_IP}/progress
```

```json
{
    "byte_current": "0",
    "byte_target": "100",
    "layer_current": "0",
    "layer_target": "0"
}
```

```shell
curl http://127.0.0.1:${PORT}/api/execute/${PRINTER_IP}/temperature
```

```json
{
    "bed_t_current": "24.2",
    "bed_t_target": "0.0",
    "t0_current": "24.8",
    "t0_target": "0.0",
    "t1_current": "0.0",
    "t1_target": "0.0"
}
```

```shell
curl http://127.0.0.1:${PORT}/api/execute/${PRINTER_IP}/position
```

```json
{
    "a_pos": "0.000",
    "b_pos": "0",
    "x_pos": "0.000",
    "y_pos": "0.000",
    "z_pos": "0.000"
}
```

```shell
curl http://127.0.0.1:${PORT}/api/execute/${PRINTER_IP}/info
```

```json
{
    "build_volume_x": "220",
    "build_volume_y": "220",
    "build_volume_z": "220",
    "firmware": " v2.4.5",
    "mac_address": "00:00:00:00:00:00",
    "machine_name": "Adventurer 5M Pro",
    "machine_type": "Flashforge Adventurer 5M Pro",
    "serial_number": "XXXXXXX0X00000",
    "tool_count": "1"
}
```

```shell
curl http://127.0.0.1:${PORT}/api/execute/${PRINTER_IP}/status
```

```json
{
    "current_file": "",
    "endstop_x_max": "110",
    "endstop_y_max": "110",
    "endstop_z_min": "0",
    "led": "1",
    "machine_status": "READY",
    "move_mode": "READY",
    "status_f": "0",
    "status_j": "0",
    "status_l": "0",
    "status_s": "1"
}
```

```shell
curl http://127.0.0.1:${PORT}/api/execute/${PRINTER_IP}/hello
```

```json
{
    "message": "Control Success V2.1."
}
```
