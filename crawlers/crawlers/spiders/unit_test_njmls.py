import unittest
import os
from njmls import Njmls
from scrapy.http import HtmlResponse

class TestNjmls(unittest.TestCase):
    
    def setUp(self):
        self.mls = Njmls()
    
    def test_get_total_pages(self):
        curdir = os.path.dirname( os.path.realpath( __file__ ) )
        file_name = 'unit_test_files/multi-page.html' 
        body = open( os.path.join(curdir, file_name ) ).read()

        response = HtmlResponse( url = 'test.com', body = body )

        self.assertEqual( 6, self.mls.get_total_pages( response ) )


    def test_list_sold(self):
        curdir = os.path.dirname( os.path.realpath( __file__ ) )
        file_name = 'unit_test_files/njmls_sold.html' 
        body = open( os.path.join(curdir, file_name ) ).read()

        houseData, mlsHist, image_links = self.mls.extract_detail_page( body, True )
        expect_house= {
        'style': u'2fam', 
        'bathrooms': 3.0, 
        'bedrooms': 5.0, 
        'tax': 9335.0, 
        'garage': u'carport,detached,1 car', 
        'listagent': {'name': u'dominik chyzy', 'tel': u'(973) 980-8382'},
        'rooms': 8.0, 
        'basement': u'full,unfinished', 
        'address': u'16 jordan ave',
        }

        self.assertEqual( expect_house, houseData)
        
        expect_mlshist= [
        {'date': u'07/26/16', 'mls': u'1611634', 'price': 447000.0, 'status': u'sold'}, 
        {'date': u'05/03/16', 'mls': u'1611634', 'price': 459000.0, 'status': u'under contract'}, 
        {'date': u'03/25/16', 'mls': u'1611634', 'price': 459000.0, 'status': u'listed'}
        ]
        self.assertEqual( expect_mlshist, mlsHist )

        for i in range(1, 16):
            self.assertEqual( 'http://pxlimages.xmlsweb.com/njmls/m/images/1611634.%d.jpg' % i, image_links[i-1] )

    def test_under_contract(self):
        curdir = os.path.dirname( os.path.realpath( __file__ ) )
        file_name = 'unit_test_files/njmls_under_contract.html' 
        body = open( os.path.join(curdir, file_name ) ).read()

        houseData, mlsHist, image_links = self.mls.extract_detail_page( body, False )

        expect_house={'style': u'2fam', 'bathrooms': 3.0, 'bedrooms': 7.0, 'tax': 8449.0, 'garage': u'3+car,park space', 'rooms': 14.0, 'basement': u'finished,full', 'address': u'23 park row'}

        self.assertEqual( expect_house, houseData )

        expect_mlshist=[
        {'date': u'07/21/16', 'mls': u'1603261', 'price': 469900.0, 'status': u'under contract'}, 
        {'date': u'06/01/16', 'mls': u'1603261', 'price': 469900.0, 'status': u'price change'}, 
        {'date': u'05/09/16', 'mls': u'1603261', 'price': 474900.0, 'status': u'price change'}, 
        {'date': u'04/11/16', 'mls': u'1603261', 'price': 485900.0, 'status': u'price change'}, 
        {'date': u'01/29/16', 'mls': u'1603261', 'price': 495900.0, 'status': u'listed'}
        ]

        self.assertEqual( expect_mlshist, mlsHist )

    def test_parse_detail_page(self):
        curdir = os.path.dirname( os.path.realpath( __file__ ) )
        file_name = 'unit_test_files/njmls_detail_page_1608743.html' 
        body = open( os.path.join(curdir, file_name ) ).read()

        
        houseData, mlsHist, image_links = self.mls.extract_detail_page( body, False )

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

    
    def test_parse_rental_active(self):

        curdir = os.path.dirname( os.path.realpath( __file__ ) )
        file_name = 'unit_test_files/njmls_rental_active.html' 
        body = open( os.path.join(curdir, file_name ) ).read()

        houseData, mlsHist, image_links = self.mls.extract_detail_page( body, False )

        self.assertEqual('cats prohbtd, dogs prohbtd, none', houseData['pets'] )
        self.assertEqual('ov/rang/gs, water', houseData['provided'] )

        self.assertEqual( [
        {'date': u'07/06/16', 'mls': u'1628335', 'price': 1600.0, 'status': u'listed'}, 
        {'date': u'07/17/12', 'mls': u'1213646', 'price': 1200.0, 'status': u'off-market'}, 
        {'date': u'04/16/12', 'mls': u'1213646', 'price': 1200.0, 'status': u'listed'}
        ], mlsHist )
