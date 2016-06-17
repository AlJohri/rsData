#!/usr/bin/env python 
import sqlite3 as sql 
import sys
import logging
import logging.handlers

class DBAccessor(object):

    def __init__(self, dbname) :
        self.dbname = dbname

    
    def isMLSExisted(self, mls):
        with sql.connect(self.DBNAME) as conn:
            cursor= conn.cursor()
            cmd = 'select count(mls) from houses where mls =?'
            r = cursor.execute(cmd, (mls,))
            if r.fetchone()[0] > 0:
                return True
            else:
                return False
    
    def getSelect(self, cmd, values=()):

        with sql.connect(self.DBNAME) as conn:
            cursor= conn.cursor()
            if values:
                r = cursor.execute(cmd, values)
            else:
                r = cursor.execute(cmd)
            return r.fetchall() 
        

        

    def insertMLS(self, mls):
        with sql.connect(self.DBNAME) as conn:
            cursor= conn.cursor()

            cmd1 = 'insert into houses (mls) values (?)'
            cursor.execute(cmd1, (mls,))

            cmd2 = 'insert into price (mls) values (?)'
            cursor.execute(cmd2, (mls,))
    
    def updateHouseInfo(self, mls, key, value):
        with sql.connect(self.DBNAME) as conn:
            cursor= conn.cursor()

            if key not in self.houseKeys:
                self.logger.error("update %s: unkown key %s" % (mls, key) )
            else:
                cmd = 'update houses set %s=? where mls=?' % key
                cursor.execute(cmd, (value, mls))

    def updatePriceInfo(self, mls, key, value):
        with sql.connect(self.DBNAME) as conn:
            cursor= conn.cursor()

            if key not in self.priceKeys:
                self.logger.error("update %s: unkown key %s" % (mls, key) )
            else:
                cmd = 'update price set %s=? where mls=?' % key
                cursor.execute(cmd, (value, mls))
    
    def runCrawler(self, crawler):
        crawler.update(self)


if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print >> sys.stderr, "table list: houses, price"
        sys.exit(1)
    
    LOG_FILENAME="houseDB.log"

    handler= logging.handlers.RotatingFileHandler(
                             LOG_FILENAME,
                             maxBytes=10000000,
                             backupCount=5)
    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    db= DBAccessor(handler) 
    funs={"houses": db.reCreateHouseTable , "price": db.reCreatePriceTable }
    
    

    for i in sys.argv[1:]:
        if funs.has_key(i):
            funs[i]()
        else:
            print >> sys.stderr, "unknow table name %s " % i





