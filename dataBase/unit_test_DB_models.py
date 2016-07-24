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

