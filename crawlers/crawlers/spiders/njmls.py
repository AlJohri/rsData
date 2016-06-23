import scrapy
from requests import Request
import  njmls_query_cfg as qc
from crawlers.items import HouseItem, MlsHistoryItem


class Njmls(scrapy.Spider):
    name = "njmls"
    allowed_domains = ['njmls.com']
    URL_LISTINGS='http://www.njmls.com/listings/index.cfm'
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36' 
    }

    def start_requests(self):
        for line in qc.Cities.strip().split('\n'):
            for proptype in qc.Proptyes:
                for stat in qc.Statuses:
                    city, zipcode = line.split()
                    query = \
                    {
                
                    'zoomlevel':0,
                    'action':'xhr.results.view.list',
                    'page':1,
                    'display':10,
                    'sortBy':'newest',
                    'location':'',
                    'city': city,
                    'state':'NJ',
                    'county':'',
                    'zipcode': zipcode,
                    'radius':'',
                    'proptype':',%s' % proptype,
                    'maxprice':'',
                    'minprice':'',
                    'beds':'',
                    'baths':'',
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
                    'status':stat,
                    }

                    houseData = HouseItem()
                    houseData['town'] = city.lower()
                    houseData['state'] = 'nj'
                    houseData['zipcode'] = zipcode

                    url = Request('GET', Njmls.URL_LISTINGS, params = query, headers = Njmls.headers ).prepare().url

                    request =  scrapy.Request( url  ) 
                    request.meta['data'] = houseData
                    yield request
        
    
    def parse(self, response):

        mlses = response.xpath('//div[@class]').re('houseresults listingrecord.*mls_number: \'(\d+)')

        for mls in mlses:
            
            query = {
            'action' : 'dsp.info',
            'mlsnum' :  mls,
            }

            houseData = response.meta['data'].copy()
            houseData['mls'] = mls

            url = Request('GET', Njmls.URL_LISTINGS, params = query, headers = Njmls.headers ).prepare().url
            request = scrapy.Request( url, meta = houseData , callback =  self.parse_njmls_site )
            request.meta['data'] = houseData
            yield request
            



    def parse_njmls_site(self, response ):
        
        houseData = response.meta['data']

        with open('%s.html' % houseData['mls'],'wa' ) as f:
            f.write(response.body)

        yield houseData

        
