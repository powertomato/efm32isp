efm32isp
========

WTF?
----

EFM32 UART programmer, see application note 3 (http://downloads.energymicro.com/an/pdf/an0003_efm32_serial_bootloader.pdf)

Prerequisites
-------------

 * python2 v2.7 or newer (xmodem and pyserial are not python3 compatible!)
 * xmodem-library (https://pypi.python.org/pypi/xmodem)
 * pyserial (https://pypi.python.org/pypi/pyserial)
 * docopt (https://pypi.python.org/pypi/docopt/0.6.1)

Usage
-----

```
    Usage:
        efm32isp [options] <binfile>

    Options:
        -h --help                 Prints this help message
        -p <port>, --port=<port>  Sets the UART port, any valid pyserial string is possible [default: /dev/ttyUSB0].
        -b <port>, --baud=<baud>  Sets the UART baud rate [default: 57600].
```
