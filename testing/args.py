import argparse

parser = argparse.ArgumentParser(description='log data from brewlogger')
parser.add_argument('-v','--verbose',action='store_true',help='print detailed info to stdout')
parser.add_argument('-l', '--log', default='/dev/null',help='writes detailed info FILE',type=file,metavar='FILE')

args = parser.parse_args()


print args.log,args.verbose
