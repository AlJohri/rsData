#!/usr/bin/env python 
import sqlite3 as sql 
import sys
import defs
import logging


logger = logging.getLogger(__name__)

class DBAccessError(Exception):
    pass

class DBAccessor(object):

    def __init__(self, dbname='') :
        self.dbname = dbname if dbname else defs.DBname
    
    def get_db_name(self):
        return self.dbname
    
    def open(self):
        self.conn = sql.connect(self.dbname )
        self.cursor = self.conn.cursor()

        logger.info('open db %s' % self.dbname )

    def close(self):
        self.conn.commit()
        self.conn.close()

        logger.info('close db %s' % self.dbname )
        
    
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close() 


    
    def update_table(self, tablename, key, value ):
        
        cmd = 'insert into %s (%s) values (?)' % ( tablename, key )
        self.cursor.execute( cmd, (value, ) )
        self.conn.commit()

#    def isMLSExisted(self, mls):
#        with sql.connect(self.dbname) as conn:
#            cursor= conn.cursor()
#            cmd = 'select count(mls) from houses where mls =?'
#            r = cursor.execute(cmd, (mls,))
#            if r.fetchone()[0] > 0:
#                return True
#            else:
#                return False
#    
#    def getSelect(self, cmd, values=()):
#
#        with sql.connect(self.dbname) as conn:
#            cursor= conn.cursor()
#            if values:
#                r = cursor.execute(cmd, values)
#            else:
#                r = cursor.execute(cmd)
#            return r.fetchall() 
#        
#
#        
#
#    def insertMLS(self, mls):
#        with sql.connect(self.dbname) as conn:
#            cursor= conn.cursor()
#
#            cmd1 = 'insert into houses (mls) values (?)'
#            cursor.execute(cmd1, (mls,))
#
#            cmd2 = 'insert into price (mls) values (?)'
#            cursor.execute(cmd2, (mls,))
#    
#    def updateHouseInfo(self, mls, key, value):
#        with sql.connect(self.dbname) as conn:
#            cursor= conn.cursor()
#
#            if key not in self.houseKeys:
#                self.logger.error("update %s: unkown key %s" % (mls, key) )
#            else:
#                cmd = 'update houses set %s=? where mls=?' % key
#                cursor.execute(cmd, (value, mls))
#
#    def updatePriceInfo(self, mls, key, value):
#        with sql.connect(self.dbname) as conn:
#            cursor= conn.cursor()
#
#            if key not in self.priceKeys:
#                self.logger.error("update %s: unkown key %s" % (mls, key) )
#            else:
#                cmd = 'update price set %s=? where mls=?' % key
#                cursor.execute(cmd, (value, mls))
#    
