#!/usr/bin/python
import MySQLdb as mdb
import sys
from xbee import XBee
import serial
import time
import struct
import traceback
import argparse


verbose = False
logfile = None
debug = False

con = mdb.connect('localhost','logger','brewing','brewlog')
cur = con.cursor()
serial_port = serial.Serial('/dev/ttyUSB0', 9600)
WINE_ADDR = b"\x12\x36"
TEMP = b"1"
HUMID = b"2"
xb = XBee(serial_port)

INSERT_CMD = "insert into winecellar values(null,now(),%f,%f);"

def logz(message):
    if verbose:
        print message
    if logfile:
        logfile.write(message)
        logfile.flush()


#end logz

def getSomething(cmd,addr):

    gotit = False
    tries = 0
    thing = -1
    while not gotit and tries <= 5:
        tries += 1
        xb.send("tx", dest_addr=addr, data=cmd)
        xb.send("tx", dest_addr=addr, data=cmd)
        response = xb.wait_read_frame(5)
        if not response:
            logz("t")
            continue
        packet = response['rf_data']

        xcmd = str(struct.unpack('b',packet[0])[0])
        thing = struct.unpack('f',packet[1:5])[0]
        gotit = xcmd == cmd

        if not gotit:
            logz("didn't get it\n")
            logz(str( cmd)+str(xcmd)+str(thing))
            time.sleep(1)
    
    return thing if gotit else -1
#end gotSomething
def main():
    try:
        while True:

            logz( "get temp: ")
            tempC = getSomething(TEMP,WINE_ADDR) 
            tempF = tempC * 9/5 + 32
            logz("%f\n"%(tempF))
            if tempC == -1:
                continue

            time.sleep(5)

            logz( "get humid: ")
            humid = getSomething(HUMID,WINE_ADDR)
            logz("%f\n"%(humid))
            if humid == -1:
                continue


            if not debug:
                logz( "logged @ %s\n"%(time.strftime('%b-%d %H:%M:%S')))

                try:    
                    cur.execute(INSERT_CMD%(humid,tempF))
                    time.sleep(15*60)
                except mdb.Error, e:
                    logz( "error %d: %s\n" % (e.args[0],e.args[1]))
                    sys.exit(1)
            else:
                time.sleep(5)
    except:
        if verbose: traceback.print_exc()
        if con:
            con.close()
#end main

 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='log data from brewlogger')
    parser.add_argument('-v','--verbose',action='store_true',help='print detailed info to stdout')
    parser.add_argument('-d','--debug',action='store_true',help='don\'t log data to mysql')
    parser.add_argument('-l', '--log',help='writes detailed info FILE',type=str,metavar='FILE')

    args = parser.parse_args()
    verbose = args.verbose
    logfile = args.log
    debug = args.debug

    # open file
    if logfile:
        logfile = open(logfile,'a')
        logfile.write("\nstarted logging at %s\n"%(time.ctime()))
        


    main()
   
 
