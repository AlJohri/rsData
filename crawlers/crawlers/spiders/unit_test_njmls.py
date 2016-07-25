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
        
        houseData, mlsHist, image_links = self.mls.extract_detail_page( body )

        expected_rlt={
        'bathrooms': 2.0, 
        'heatcool': u'baseboard, gas', 
        'bedrooms': 4.0, 
        'tax': 7377.0, 
        'garage': u'o/see remk,park space', 
        'yearbuilt': 1960, 
        'rooms': 11.0, 
        'basement': u'full,prt finished', 
        'address': u'313 6th st',
        'style': u'2fam',
        'utility': u'sep elec, sep gas, sep heat',
        }
        
        self.assertEqual( expected_rlt, houseData )

        expected_hist= [
        {'status': 'price change', 'mls': '1608743', 'date': '06/06/16', 'price': 488000.0}, 
        {'status': 'listed', 'mls': '1608743', 'date': '03/04/16', 'price': 498000.0}, 
        {'status': 'off-market', 'mls': '9981576', 'date': '10/31/99', 'price': 239900.0}, 
        {'status': 'listed', 'mls': '9981576', 'date': '09/13/99', 'price': 239900.0}
        ]

        self.assertEqual( expected_hist, mlsHist )
        
        expected_image_links = [
            "http://pxlimages.xmlsweb.com/njmls/m/images/1608743.1.jpg", 
            "http://pxlimages.xmlsweb.com/njmls/m/images/1608743.2.jpg", 
            "http://pxlimages.xmlsweb.com/njmls/m/images/1608743.3.jpg", 
            "http://pxlimages.xmlsweb.com/njmls/m/images/1608743.4.jpg", 
            "http://pxlimages.xmlsweb.com/njmls/m/images/1608743.5.jpg", 
            "http://pxlimages.xmlsweb.com/njmls/m/images/1608743.6.jpg", 
            ]

        self.assertEqual( expected_image_links, image_links )


