#!/usr/bin/env python
# create Database 

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
        pass

    
    def __call__( self, cursor):
        pass

        


def createTables( dbname, funs ):
    with sql.connect( dbname ) as conn:
        cursor = conn.cursor()
        for fun in funs:
            fun(cursor)



def main():
    usage = 'usage: %prog [options] dbname'
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    dbname = args[0]
    
    tables = [ SqlTable( table_name, schema ) for table_name, schema in Schemas.items() ]
    
    createTables( dbname, tables )

    

main()

