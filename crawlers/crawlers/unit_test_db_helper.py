import unittest
from  DB_models import database, House, Agent, Mlsinfo, Housemls, Mlshistory
import os
from db_helper import get_next_dummy_address

class TestDB_helper(unittest.TestCase):
    
    def setUp(self):
        curdir = os.path.dirname( os.path.realpath( __file__ ) )
        self.dbname = './unit_test_files/temp.db'
        self.dbname = os.path.join(curdir, self.dbname ) 

        database.init( self.dbname )  
        database.create_tables([House, ])


    def tearDown(self):
        database.close()
        os.remove( self.dbname )

    def test_dummpy_address(self):
        
        self.assertEqual('nxstd-1', get_next_dummy_address() )

        House.create( address='nxstd-1', state = 'n', town ='n', zipcode = 'n' )

        House.create( address='nxstd-110', state = 'n', town ='n', zipcode = 'n' )

        self.assertEqual('nxstd-111', get_next_dummy_address() )


