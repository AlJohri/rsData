import requests
from bs4 import BeautifulSoup as bs
import logging 
import json
import re
import random
import copy

Logger = logging.getLogger(__name__)


def saveRequest(page, fn='tmp.html'):
    fd=open(fn, 'w')
    fd.write(page.text.encode('utf-8'))
    fd.close()


class NJMLS(object):
    URL_LISTINGS='http://www.njmls.com/listings/index.cfm'

    def __init__(self ):
        self.session= requests.Session()
        
    def testResonse(self, r):
        if r.ok:
            Logger.info("Connection success: %s", r.url )
        else:
            Logger.info("Connection failed: %s", r.url )

        return r.ok
        

    def getListingNJMLS(self, city, maxn=50 ):
        '''
        Return a list of active NLMS from a city in NJ
        '''

        query = \
        {
    
        'zoomlevel':0,
        'action':'xhr.results.view.list',
        'page':1,
        'display':50,
        'sortBy':'newest',
        'location':'',
        'city':'CARLSTADT,EAST RUTHERFORD,HASBROUCK HEIGHTS,LYNDHURST,RUTHERFORD,WALLINGTON',
        'state':'NJ,NJ,NJ,NJ,NJ,NJ',
        'county':'BERGEN,BERGEN,BERGEN,BERGEN,BERGEN,BERGEN',
        'zipcode':'07072,07073,07604,07071,07070,07057',
        'radius':'',
        'proptype':',2',
        'maxprice':400000,
        'minprice':'',
        'beds':0,
        'baths':0,
        'dayssince':'',
        'newlistings':'',
        'pricechanged':'',
        'keywords':'',
        'mls_number':'',
        'garage':'',
        'basement':'',
        'fireplace':'',
        'pool':'',
        'yearBuilt':'',
        'building':'',
        'officeID':'',
        'openhouse':'',
        'countysearch':'false',
        'ohdate':'',
        'style':'',
        'emailalert_yn':'N',
        'status':'A'
   
        }

        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36' 
        }


        r= self.session.get(NJMLS.URL_LISTINGS, params= query, headers= headers ) 
        
        if not self.testResonse(r):
            raise RuntimeError( r )

        saveRequest(r)
        return r
            
        
if __name__ == '__main__':

    web = NJMLS()
    web.getListingNJMLS('carlstadt')


