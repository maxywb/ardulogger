#!/usr/bin/python
import MySQLdb as mdb
import sys

con = None


try:

    con = mdb.connect('localhost','logger','brewing','brewlog')

    cur = con.cursor()
    
    rows = cur.fetchall()

    for row in rows:
        print row


except mdb.Error, e:
    print "error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
