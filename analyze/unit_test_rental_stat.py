import unittest
from rental_stat import RentRecord, parseTable


lines = \
'''
1714944 |sell |2017-09-11|145|  455000|BOM | 5.0| 2.0|   12079|                      541 market st|   elmwood park
1719532 |sell |2017-09-11|119|  475000|PC  | 7.0| 3.0|   12043|                       1466 71st st|   north bergen

'''

class Test_Rental_stat(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parseTable(self):
        
        rlt = parseTable( lines.split('\n' ) )
        print rlt  


