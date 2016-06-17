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
        query = {
        'action': 'dsp.results',
        'city': city,
        'state': 'NJ',
        'status': 'A'
        }


        r= self.session.get(NJMLS.URL_LISTINGS, params= query ) 
        
        if not self.testResonse(r):
            raise RuntimeError( r )
            
        
        saveRequest(r)
if __name__ == '__main__':

    web = NJMLS()
    web.login()
    web.getListingNJMLS('carlstadt'.upper())


