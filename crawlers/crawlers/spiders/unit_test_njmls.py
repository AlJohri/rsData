import unittest
import os
from njmls import Njmls

class TestNjmls(unittest.TestCase):
    
    def setUp(self):
        self.mls = Njmls()
    
    def test_parse_detail_page(self):
        curdir = os.path.dirname( os.path.realpath( __file__ ) )
        file_name = 'unit_test_files/njmls_detail_page_1608743.html' 
        body = open( os.path.join(curdir, file_name ) ).read()
        
        houseData, mlsHist= self.mls.extract_detail_page( body )

        expected_rlt={
        'bathrooms': 2.0, 
        'heatcool': u'Baseboard, Gas', 
        'bedrooms': 4.0, 
        'tax': 7377.0, 
        'garage': u'O/See Remk,Park Space', 
        'yearbuilt': 1960, 
        'rooms': 11.0, 
        'basement': u'Full,Prt Finished', 
        'address': u'313  6th St',
        }
        
        self.assertEqual( expected_rlt, houseData )

        expected_hist= [
        {'status': 'Price change', 'mls': '1608743', 'date': '06/06/16', 'price': 488000.0}, 
        {'status': 'Listed', 'mls': '1608743', 'date': '03/04/16', 'price': 498000.0}, 
        {'status': 'Off-market', 'mls': '9981576', 'date': '10/31/99', 'price': 239900.0}, 
        {'status': 'Listed', 'mls': '9981576', 'date': '09/13/99', 'price': 239900.0}
        ]

        self.assertEqual( expected_hist, mlsHist )



