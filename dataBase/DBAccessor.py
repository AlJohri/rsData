#!/usr/bin/env python 
import sqlite3 as sql 
import sys
import logging
import logging.handlers

class DBAccessor(object):

    def __init__(self, logHandler, logLevel=logging.INFO):
        self.DBNAME='houseData.db'
        self.houseKeys=[
            "mls",
            "address",
            "town", 
            "state",
            "status",
            "listdate",
            "solddate",
            "commutetime",
            "style",
            "category",
            "lot",
            "floor",
            "rooms",
            "bedrooms",
            "bathrooms",
            "basement",
            "garage",
            "heatcool",
            'yearbuilt'
            ]

        self.priceKeys=[
            "mls",
            "price",
            "tax",  
            "rent1",
            "rent2",
            "rent3",
            ]


        self.logger = logging.getLogger('HouseDB')
        self.logger.setLevel(logLevel)
        self.logger.addHandler(logHandler)

    def reCreateHouseTable(self):
        
        with sql.connect(self.DBNAME) as conn:
            cursor= conn.cursor()
        
            cursor.execute('drop table if exists houses;')
            cursor.execute( 
            '''
            create table houses (  
                mls text primary key,
                address text,
                town text, 
                state text,
                status text,  /* A: active, S: sold*/
                listdate date,
                solddate date,
                commutetime real,
                style text,
                category text,
                lot real,
                floor real,
                rooms real,
                bedrooms real,
                bathrooms real, 
                basement text,
                garage text,
                heatcool text,
                yearbuilt integer
            );
            ''')

    def reCreatePriceTable(self):
        with sql.connect(self.DBNAME) as conn:
            cursor= conn.cursor()

            cursor.execute('drop table if exists price;' )
            cursor.execute( 
            '''
            create table price (  
                mls text,
                price real,
                tax real,  
                rent1  real,
                rent2  real,
                rent3  real,
                foreign key (mls) references houses(mls)  on update cascade on delete cascade
            );
            ''')
    
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





