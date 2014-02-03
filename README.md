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

Usage
-----

'''efm32isp.py [-h] [-p PORT] [-b BAUD] binfile'''

#positional arguments:
'''  binfile               Path to the binary to flash'''

#optional arguments:
'''
  -h, --help            show this help message and exit
  -p PORT, --port PORT  The UART port, (any valid pyserial string),
                        default=/dev/ttyUSB0
  -b BAUD, --baud BAUD  Baud rate to use, default=57600
'''
