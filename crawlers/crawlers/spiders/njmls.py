import scrapy
from requests import Request
from bs4 import BeautifulSoup as bs
import locale
import re
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
        
        houseRlt, mls_histories = self.extract_detail_page(response.body )
        houseData['address'] = houseRlt['address']
        houseData['bathrooms'] = houseRlt['bathrooms']
        houseData['bedrooms'] = houseRlt['bedrooms']
        houseData['rooms'] = houseRlt['rooms']
        houseData['basement'] = houseRlt['basement']
        houseData['yearbuilt'] = houseRlt['yearbuilt']
        houseData['heatcool'] = houseRlt['heatcool']
        houseData['tax'] = houseRlt['tax']

        yield houseData

        for history in mls_histories: 
            
            data = MlsHistoryItem()
            data['mls'] = history['mls']
            data['date'] = history['date']
            data['price'] = history['price']
            data['status'] = history['status']
            yield data



        
    def extract_detail_page(self, html):
        
        houseRlt={}
        soup = bs(html)
        listSection= soup.find('div', {'id': 'listsection'})
        contents = listSection.findAll('strong')
        
        locale.setlocale(locale.LC_ALL, "")

        for content in contents:
            key= content.string.strip()
            value= content.nextSibling.strip()


            if re.search(r'^Address', key):
                houseRlt['address'] = value
        
            elif re.search(r'^Rooms', key):
                houseRlt['rooms'] = float(value)

            elif re.search(r'^Bedrooms', key):
                houseRlt['bedrooms'] = float(value)

            elif re.search(r'^Full Baths', key):
                houseRlt['bathrooms'] = houseRlt.get('bathrooms', 0) + float(value)

            elif re.search(r'^Half Baths', key):
                houseRlt['bathrooms'] = houseRlt.get('bathrooms', 0) + float(value)*0.5

            elif re.search(r'^Basement', key):
                houseRlt['basement'] = value

            elif re.search(r'^Garage', key):
                houseRlt['garage'] = value


            elif re.search(r'^Taxes', key):
                houseRlt['tax'] = locale.atof(value.replace('$',''))

            else:
                pass
        

        features= soup.find('div', {'id':'listingfeatures'})
        features = features.findAll('strong')
        for f in features:
            key= f.string.strip()
            value = f.nextSibling.nextSibling.strip()

            if re.search(r'^Heat', key):
                houseRlt['heatcool'] = value

            elif re.search(r'^Year', key):
                houseRlt['yearbuilt']= int(re.search(r'(\d+)', value).group(0))
            else:
                pass
        

        mls_history = []
        mls_prev = ''
        data = soup.find('div', {'class': "nj-grid-body nj-history-body" } )
        for row in data.findAll('div', {'class': 'nj-row' }):
            mls = row.find('div', {'class': 'mls-num' } ).text.strip()
            if mls == '':
                mls = mls_prev
            date = row.find('div', {'class': 'mls-date' } ).text.strip()
            price = row.find('div', {'class': 'mls-price' } ).text.strip()
            price = locale.atof(price.replace('$',''))
            status = row.find('div', {'class': 'mls-status' } ).text.strip()
            mls_history.append({
            'mls': mls,
            'date': date,
            'price': price,
            'status': status
            })


            mls_prev = mls

        return (houseRlt, mls_history )
