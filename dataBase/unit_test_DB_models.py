import unittest
import peewee
from  DB_models import database, House, Mlsinfo, Housemls, Mlshistory
import os

class TestDBModels(unittest.TestCase):
    
    def setUp(self):
        self.dbname = './unit_test_files/temp.db'
        database.init( self.dbname )  
        database.create_tables([House, Mlsinfo, Housemls, Mlshistory])


    def tearDown(self):
        os.remove( self.dbname )

    def test_house_table(self):
        house = House.create(address= '120 13th',
                             town = 'newark', 
                             state = 'nj'
                             )
        house.save()
        for h in House.select():
            print h.address, h.houseid, h.state, h.town
