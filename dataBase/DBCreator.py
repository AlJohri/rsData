#!/usr/bin/env python
# create Database 
# This file is modified by Cherry
import sys
from optparse import OptionParser
from collections import OrderedDict
import defs
import DB_models

Schemas = OrderedDict()

Schemas['House']      = DB_models.House
Schemas['Mlsinfo']    = DB_models.Mlsinfo
Schemas['Housemls']   = DB_models.Housemls
Schemas['Mlshistory'] = DB_models.Mlshistory


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
	if len(args) > 1:
		parser.print_help()
		sys.exit(1)
        elif len(args) == 1:
            dbname = args[0]
            DB_models.database.init(dbname)
        else:
            dbname = defs.DBname
	
        if not options.table:
                options.table = Schemas.keys()
        for table_name in options.table:
                if not Schemas.get(table_name, False):
                        print >> sys.stderr,"Table: %s does not exist!" %(table_name)
                else:
                        if options.force:
                            with sql.connect( dbname ) as conn:
                                conn.execute('drop table if exists %s' % ( table_name ) )

                        Schemas[table_name].create_table()
                        print >> sys.stdout, "created table %s" % table_name

    

if __name__ == "__main__":
    main()

