#!/usr/bin/env python 
import sqlite3 as sql 
import sys
import logging
import logging.handlers

conn = sql.connect('test.db')
print "Opened database successfully";

conn.execute('''CREATE TABLE housemls
       (address text primary key,
        mls text);''')
conn.execute( 
            '''
            create table houses (  
                mls text primary key,
                status text,  /* A: active, S: sold*/
                listdate date,
                solddate date,
		listprice int,
		currprice int,
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
conn.execute('''INSERT INTO housemls (address, mls) VALUES('559 summit ave carlstadt nj', '482048');''')
print "Table created successfully";
cursor = conn.execute("SELECT address, mls from housemls")
for row in cursor:
   print "address = ", row[0]
   print "mls = ", row[1], "\n"

print "Operation done successfully";
conn.close()
