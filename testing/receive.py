
from xbee import XBee
import serial
import time
import struct

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
address16 = b"\x01\x02\x03\x06"

TEMP = b"1"
HUMID = b"2"

ta = 0.0
th = 0.0
ha = 0.0
hh = 0.0


xb = XBee(serial_port)
while True:


    response = xb.wait_read_frame(2)

    if response:
        print response

