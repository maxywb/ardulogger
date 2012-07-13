
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
    xb.send("tx", dest_addr=b"\x12\x36", data=TEMP)
    xb.send("tx", dest_addr=b"\x12\x36", data=TEMP)
    xb.send("tx", dest_addr=b"\x12\x36", data=TEMP)
    xb.send("tx", dest_addr=b"\x12\x36", data=TEMP)
    response = xb.wait_read_frame(5)
    ta +=1
    if response:
        packet = response['rf_data']
        cmd = struct.unpack('b',packet[0])[0]
        tempC = struct.unpack('f',packet[1:5])[0]
        th +=1

    time.sleep(10)

    xb.send("tx", dest_addr=b"\x12\x36", data=HUMID)
    xb.send("tx", dest_addr=b"\x12\x36", data=HUMID)
    xb.send("tx", dest_addr=b"\x12\x36", data=HUMID)
    xb.send("tx", dest_addr=b"\x12\x36", data=HUMID)
    response = xb.wait_read_frame(5)
    ha += 1
    if response:
        packet = response['rf_data']
        cmd = struct.unpack('b',packet[0])[0]
        humid = struct.unpack('f',packet[1:5])[0]
        hh +=1

    

    import os
    os.system( 'clear' )

    #print chr(27) + "[2J"
    print "temp: (%f,%d) :: humid: (%f,%d)"%((th/ta),ta,(hh/ha),ha)
    time.sleep(10)
