# Документация

Известные коды управления принтером:

| Код          | Действие                            |
|--------------|-------------------------------------|
| ~M27\r\n     | Получить данные о прогрессе печати  |
| ~M105\r\n    | Получить данные о температуре       |
| ~M114\r\n    | Получить позицию печатающей головки |
| ~M115\r\n    | Получить информацию о принтере      |
| ~M119\r\n    | Получить текущий статус принтера    |
| ~M601 S1\r\n | Приветствие для начала работы       |

Кандидаты на проверку:

| Код                      | Действие                      |
|--------------------------|-------------------------------|
| ~M23\r\n                 | Печать с SD карты?            |
| ~M24\r\n                 | Продолжить после паузы?       |
| ~M25\r\n                 | Пауза?                        |
| ~M26\r\n                 | Остановить печать?            |
| ~M28\r\n                 | Начать запись на SD карту?    |
| ~M29\r\n                 | Закончить запись на SD карту? |
| ~G28\r\n                 | Home?                         |
| ~M146 r255 g255 b255\r\n | Включить подсветку?           |
| ~M146 r0 g0 b0\r\n       | Выключить подсветку?          |
| ~M148\r\n                | Издать звук?                  |
| ~M650\r\n                | Калибровка?                   |

```
To print from file: 'M650', 'M28 <file size> 0:/user/<file name>', encode the file with base64 and then send 4096 bytes each time, 'M29', 'M23 0:/user/<file name>'

Max length for file name is 36 bytes. File size is the base64 encoded size.

Update; To send a file with TCP socket to Finder: Do not encode with base64, still send 4096 bytes at a time but add 16 bytes at the start. The first four bytes should be 0x5a, 0x5a, 0xa5, 0xa5. Next four bytes should be a four byte unsigned big endian counter starting at 0. Next four bytes should be a four byte unsigned big endian data length (4096, except last packet). The last four bytes should be a big endian CRC32 of the data for that packet. The last packet has to be padded with 0x00 until the data length is 4096 bytes. The CRC is for the data without padding.

To connect through USB I used pyusb (https://github.com/pyusb/pyusb). Search for the printer with vendor '0x2b71' and product '0x0002'. You can send commands to endpoint 0x1 and read response from endpoint 0x81. To send a file you use endpoint 0x3.
```

## Установка

Для установки нужен `docker`.

Сборка и запуск:

```shell
git clone https://github.com/IgorZyktin/FlashForgeAdventurer5MAPI.git
cd FlashForgeAdventurer5MAPI
docker build -t flashforge:v0.1 .
docker run -d -p 9876:9876 flashforge:v0.1
```

GUI доступен по адресу:

```shell
http://127.0.0.1:9876/ru/<ip адрес вашего принтера>
```

## Непосредственная работа с API

Если есть желание, вы можете вручную запрашивать данные у API.

Примеры запросов:

```shell
PRINTER_IP=192.168.1.45
curl http://127.0.0.1:9876/api/execute/${PRINTER_IP}/progress
curl http://127.0.0.1:9876/api/execute/${PRINTER_IP}/temperature
curl http://127.0.0.1:9876/api/execute/${PRINTER_IP}/position
curl http://127.0.0.1:9876/api/execute/${PRINTER_IP}/info
curl http://127.0.0.1:9876/api/execute/${PRINTER_IP}/status
curl http://127.0.0.1:9876/api/execute/${PRINTER_IP}/hello
```
