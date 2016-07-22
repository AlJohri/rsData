import unittest
from items import HouseItem, MlsHistoryItem

H = HouseItem()
H['mls'] = 'jdlai'
H.dataBaseUpdate('da')
print dir(H)


