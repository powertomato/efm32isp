#!/usr/bin/env python2

from xmodem import XMODEM
import sys,os
import time
import serial
import argparse


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
    CHK( lines[0]=='', RESP_ERR,3)
    CHK( lines[1]=='', RESP_ERR,3)
    CHK( len(lines[2])==29, RESP_ERR,3)

    version,ignore,chipid = lines[2].split(" ")
    # line 3 is glitch due to UART-baud reconfiguration of bootloader
    CHK( lines[4]=='?', RESP_ERR,4)

    INFO( "Bootloader version: '%s' ChipID: '%s'" % (version,chipid) )
    return (version,chipid)


def upload(ser,path):
    f = open(path,"rb")

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


def main(args):

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p","--port", help="The UART port, (any valid pyserial string), default=/dev/ttyUSB0")
    arg_parser.add_argument("-b","--baud", help="Baud rate to use, default=57600", type=int)
    arg_parser.add_argument("binfile", help="Path to the binary to flash")
    argp = arg_parser.parse_args()

    if not argp.port:
        argp.port = "/dev/ttyUSB0"
    if not argp.baud:
        argp.baud = 57600
    ser = serial.Serial(argp.port, argp.baud, timeout=0, parity=serial.PARITY_NONE)
    ser.open()
    if not ser.isOpen():
        sys.stderr.write("Couldn't open serial port '" + argp.port + "'!\n")
        sys.exit(1)

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
    upload(ser,argp.binfile)


    
if __name__ == "__main__":
    main(sys.argv)


#"1.60 ChipID: 20353500503EBB68"
