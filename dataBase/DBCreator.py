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
    

if __name__ == "__main__":
    main()

