import unittest
from rental_stat import RentRecord, parseTable


lines = \
'''
1407285 |rent |2014-03-29| 18|    1425|L   | 2.0| 1.0|    None|           82 hackensack st, unit 8|     wood ridge
1341076 |rent |2014-03-26|122|    1400|L   | 2.0| 1.0|    None|          74 9th st, unit 2nd floor|     wood ridge
1400888 |rent |2014-03-26| 75|    2100|L   | 3.0| 1.0|    None|                      580 union ave|     wood ridge
1405117 |rent |2014-03-24| 32|    1250|L   | 1.0| 1.0|    None|         176 hackensack st, unit 16|     wood ridge
'''

class Test_Rental_stat(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parseTable(self):
        
        rlt = parseTable( lines.split('\n' ) )
        print rlt  


