#!/usr/bin/env python
# create Database 
# This file is modified by Cherry
import sqlite3 as sql
import sys
from optparse import OptionParser

# table name to schema mapping
Schemas= {   
'housemls':
	    '''
	    houseID int,
            mls text,
            FOREIGN KEY (houseID) REFERENCES houses(houseID)
            ''',

'houses':
	    '''
            houseID int primary key,
	    address text,
            town text, 
            state text,
            category text,
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
            rent int,
            images blob,
            CONSTRAINT uniqAddress  UNIQUE ( address, town, state )
            ''',
    

'mlshistory':
	    '''
            mls text,
	    Date date,
	    Price int,
	    status text
	    '''
}

class SqlTable(object):
    
    def __init__(self, table_name, schema ):
        self.table_name = table_name
        self.schema = schema

    
    def create( self, cursor):
        cursor.execute('create table %s (%s)' % ( self.table_name, self.schema ))
        
    def delete( self, cursor):
        cursor.execute('drop table if exists %s' % ( self.table_name ))

def foo_callback(option, opt, value, parser):
	setattr(parser.values, option.dest, value.split(','))

def main():
	usage = 'usage: %prog [options] dbname'
	parser = OptionParser(usage=usage)
	parser.add_option("-l", "--lial", action="store_true", dest="list", default = False, help= "list all tables")
	parser.add_option("-f", "--force", action="store_true", dest="force", default = False, help= "force remove and create tables")
	parser.add_option("-t", "--table", type="string", action='callback', callback=foo_callback, help="list of the table", dest="table")
	(options, args) = parser.parse_args()
	if options.list:    
		print "Tables in schemas are: " + str(Schemas.keys())
		sys.exit(1)
	if len(args) != 1:
		parser.print_help()
		sys.exit(1)

	dbname = args[0]
	
	
	with sql.connect( dbname ) as conn:
		for table_name, schema in Schemas.items():
			table_schema = SqlTable( table_name, schema )
			if options.table:
				for itera in options.table:
					if itera == table_name:
						table_schema.create(conn)
			elif options.force:
				table_schema.delete(conn)
				table_schema.create(conn)
			else:
				table_schema.create(conn)
    

if __name__ == "__main__":
    main()

