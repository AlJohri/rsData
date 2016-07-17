#!/usr/bin/env python
# create Database 
# This file is modified by Cherry
import sqlite3 as sql
import sys
from optparse import OptionParser
from collections import OrderedDict

# table name to schema mapping
Schemas= OrderedDict()    

# house id to house location map
Schemas['houses'] =\
'''
houseID int primary key,
address text,
town text, 
state text,
CONSTRAINT uniqAddress  UNIQUE ( address, town, state )
'''

# snapshot of all information for the mls.
# notice that for a location, the house can go through renovations,
# therefore, the mls the sole reference for the condition of the house that being sold 
# at the given time. 
# All relavent infomation are stored and should be enough to decide whether it is a good investment. 
Schemas['mlsInfo']=\
'''
mls text primary key,
style text,
lot real,
floor real,
rooms real,
bedrooms real,
bathrooms real,
attic text,
basement text,
garage text,
heatcool text,
utility text,
yearbuilt int,
tax  int,
schoolH int,
schoolM int,
schoolE int,
floodzone int,
estimaterent int,
images blob
'''

# a house can be listed by multiple mlses
Schemas['housemls']=\
'''
houseID int,
mls text,
FOREIGN KEY (houseID) REFERENCES houses(houseID),
FOREIGN KEY (mls) REFERENCES mlsInfo(mls)
'''

# a single mls can have multiple list status
Schemas['mlshistory']=\
'''
mls text,
Date date,
Price int,
status text,
FOREIGN KEY (mls) REFERENCES mlsInfo(mls)
'''

class SqlTable(object):
    
    def __init__(self, table_name, schema ):
        self.table_name = table_name
        self.schema = schema

    
    def create( self, cursor):
        cursor.execute('create table %s (%s)' % ( self.table_name, self.schema ))
        
    def delete( self, cursor):
        cursor.execute('drop table if exists %s' % ( self.table_name ))

def table_callback(option, opt, value, parser):
	setattr(parser.values, option.dest, value.split(','))

def main():
	usage = 'usage: %prog [options] dbname'
	parser = OptionParser(usage=usage)
	parser.add_option("-l", "--lial", action="store_true", dest="list", default = False, help= "list all tables")
	parser.add_option("-f", "--force", action="store_true", dest="force", default = False, help= "force remove and create tables")
	parser.add_option("-t", "--table", type="string", action='callback', callback=table_callback, help="list of the table", dest="table")
	(options, args) = parser.parse_args()
	if options.list:    
		print "Tables in schemas are: " + str(Schemas.keys())
		sys.exit(1)
	if len(args) != 1:
		parser.print_help()
		sys.exit(1)

	dbname = args[0]
	
	
	with sql.connect( dbname ) as conn:
		if not options.table:
			options.table = Schemas.keys()
		for itera in options.table:
			if not Schemas.get(itera, False):
				print >> sys.stderr,"Table: %s does not exist!" %(itera)
			else:
				table_schema = SqlTable(itera, Schemas[itera])
				if options.force:
					table_schema.delete(conn)
				table_schema.create(conn)
                                print >> sys.stdout, "created table %s" % itera

    

if __name__ == "__main__":
    main()

