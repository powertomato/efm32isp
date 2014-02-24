#!/usr/bin/env python2

import logging
logging.getLogger("xmodem")

from xmodem import XMODEM
import sys,os,os.path
import time
import serial
from docopt import docopt


RESP_ERR = "unexpected response!"
def ERR(msg,ecode=0):
    sys.stderr.write(msg + os.linesep)
    if( ecode!= 0):
        exit(ecode)

def INFO(msg):
    sys.stdout.write(msg + os.linesep)

def CHK(bval, msg, ecode=0):
    if not bval:
        ERR(msg,ecode)


def get_response(ser):
    answer = ""
    resp=ser.read()
    while resp != "":
        answer += resp
        resp = ser.read()
    return answer

def handle_init(resp):
    lines = resp.split("\r\n")
    while '' in lines:
        lines.remove('')

    CHK( "ChipID" in lines[0], RESP_ERR,3)

    version,ignore,chipid = lines[0].split(" ")
    INFO( "Bootloader version: '%s' ChipID: '%s'" % (version,chipid) )
    return (version,chipid)


def upload(ser,path,destructive=False):
    try:
        f = open(path,"rb")
    except IOError:
        CHK( False, "'%s': can't open file" % path,5)

    # upload command
    if destructive:
        ser.write('d')
    else:
        ser.write('u')

    def ser_write(msg,timeout=1):
        ser.setWriteTimeout(timeout)
        return ser.write(msg)

    def ser_read(size,timeout=1):
        ser.setTimeout(timeout)
        return ser.read(size)

    modem = XMODEM(ser_read, ser_write)
    modem.send(f)

    ser.setTimeout(0)
    ser.setWriteTimeout(0)

    # reset command
    ser.write('r')

def main(args):
    """
    Usage:
        efm32isp [options] <binfile>

    Options:
        -h --help                 Prints this help message
        -d                        Destructive upload, overwrites the bootloader
        -p <port>, --port=<port>  Sets the UART port, any valid pyserial string is 
                                  possible [default: /dev/ttyUSB0].
        -b <port>, --baud=<baud>  Sets the UART baud rate [default: 115200].
    """
    argp = docopt(main.__doc__,version="efm32isp 2014-02-24")
    try:
        ser = serial.Serial(argp["--port"], argp["--baud"], timeout=0, parity=serial.PARITY_NONE)
        if not ser.isOpen():
            ser.open()
    except serial.serialutil.SerialException as ex:
        ERR("Couldn't open serial port '" + argp["--port"] + "'" + os.linesep + str(ex),1)
    if not ser.isOpen():
        ERR("Couldn't open serial port '" + argp["--port"] + "'",1)

    sys.stdout.write("Put the chip into bootloader mode!\n")
    sys.stdout.write("Waiting for bootloader to respond ")
    sys.stdout.flush()
    resp = ""
    tries = 10
    while resp == "":
        #trigger auto baud rate configuration
        ser.write("U")
        time.sleep(1.0/10)
        resp = get_response(ser)
        for i in range(5):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1.0/10)
        tries -= 1
        if tries < 0:
            INFO(" ERROR")
            ERR("Bootloader not responding!",2)
    INFO("") #newline

    handle_init(resp)
    upload(ser,argp["<binfile>"],argp["-d"])



if __name__ == "__main__":
    main(sys.argv)

