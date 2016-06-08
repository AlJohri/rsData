#!/usr/bin/env python
# create Database 
# This file is modified by Cherry
import sqlite3 as sql
import sys
from optparse import OptionParser

# table name to schema mapping
Schemas= {   
'houses':
'''
''',

}

class SqlTable(object):
    
    def __init__(self, table_name, schema ):
        self.table_name = table_name
        self.schema = schema

    
    def create( self, cursor):
        pass


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

    

main()

