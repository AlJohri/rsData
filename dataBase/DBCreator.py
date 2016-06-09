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
	    houseID int primary key,
            mls text''',

'houses':
	    '''
	    address text primary key,
            town text, 
            state text,
      	    houseID int,
            style text,
            category text,
            lot text,
            floor text,
            rooms text,
            bedrooms text,
            bathrooms text,
            attic text,
            basement text,
            garage text,
            heatcool text,
            yearbuilt text,
            rent int,
            FOREIGN KEY (houseID) REFERENCES housemls(houseID)''',

'mlshistory':
	    '''
            mls text primary key,
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


def main():
    usage = 'usage: %prog [options] dbname'
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    dbname = args[0]
    
    with sql.connect( dbname ) as conn:
        for table_name, schema in Schemas.items():
            SqlTable( table_name, schema ).create(conn)
    conn.execute('''INSERT INTO housemls (houseID, mls) VALUES(559, '482048');''')
    cursor = conn.execute("SELECT houseID, mls from housemls")
    for row in cursor:
    	print "houseID = ", row[0]
    	print "mls = ", row[1], "\n"
    

main()

