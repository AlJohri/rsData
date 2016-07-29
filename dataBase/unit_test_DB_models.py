import unittest
import peewee
import DB_models
from  DB_models import database, House, Mlsinfo, Housemls, Mlshistory
from DB_models import IntegrityError
import sqlite3 as sql
import os

class TestDBModels(unittest.TestCase):
    
    def setUp(self):
        self.dbname = './unit_test_files/temp.db'
        database.init( self.dbname )  
        database.create_tables([House, Mlsinfo, Housemls, Mlshistory])


    def tearDown(self):
        database.close()
        os.remove( self.dbname )

    def test_house_table(self):
        address= '120 13th'
        town= 'newark'
        state= 'nj'
        zipcode = '07123'

        house = House.create( address = address, town = town, state = state, zipcode = zipcode)
        data =   House.get( House.state == 'nj')
        self.assertEqual( address, data.address )
        self.assertEqual( town , data.town )
        self.assertEqual( state, data.state)
        self.assertEqual( zipcode, data.zipcode)


        house_duplicate = House( address = address, town = town, state = state, zipcode = zipcode)
        with self.assertRaises( peewee.IntegrityError ):
            house_duplicate.save()
        
    def test_mls_update(self):
        
        mls = '1630289'
        mlsinfo = Mlsinfo.create( mls = mls)

        self.assertEqual(None, mlsinfo.attic )

        mlsinfo.attic = 'old' 
        mlsinfo.save()
        
        instance = Mlsinfo.get( mls = mls )
        self.assertEqual('old', instance.attic )
    
    def test_mls_history(self):
        from datetime  import date
        from datetime  import datetime
        
        mls1 = '12345'
        date1 = datetime.strptime( '12/31/14' ,  '%m/%d/%y' ).date()
        
        mls2 = '12346'
        date2 = datetime.strptime( '11/30/99', '%m/%d/%y' ).date()

        mls3 = '12347'
        date3 = datetime.strptime( '11/30/01', '%m/%d/%y' ).date()


        Mlshistory.create( mls = mls1, date = date1)
        Mlshistory.create( mls = mls2, date = date2)
        Mlshistory.create( mls = mls3, date = date3)

        d =  Mlshistory.get( Mlshistory.date > date(2012,1,1 ) )
        self.assertEqual( mls1, d.mls_id )

