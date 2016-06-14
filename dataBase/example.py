from time import strftime
from calendar import month_abbr
from optparse import OptionParser

# Set the CL options 
parser = OptionParser()
usage = "usage: %prog [options] arg1 arg2"

parser.add_option("-m", "--month", type="string",
                  help="select month from  01|02|...|12", 
          dest="mon", default=strftime("%m"))

parser.add_option("-u", "--user", type="string",
                  help="name of the user", 
          dest="vos")

options, arguments = parser.parse_args()

abbrMonth = tuple(month_abbr)[int(options.mon)]

if options.mon:
    print "The month is: %s" % abbrMonth 

if options.vos:
    print "My name is: %s" % options.vos 

if options.mon and options.vos:
    print "I'm '%s' and this month is '%s'" % (options.vos,abbrMonth)
