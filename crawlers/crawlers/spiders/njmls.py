import scrapy
from requests import Request
from bs4 import BeautifulSoup as bs
import locale
import re
import  njmls_cfg as qc
from crawlers.items import HouseItem, MlsHistoryItem, AgentItem
from scrapy.exceptions import CloseSpider

def normalize_text( text ):
    return ' '.join( text.strip().lower().split() )

class Njmls(scrapy.Spider):
    name = "njmls"
    allowed_domains = ['njmls.com']
    URL_LISTINGS='http://www.njmls.com/listings/index.cfm'
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36' 
    }

    def gen_query(self, city, zipcode, proptype, stat, page):
        query = \
        {
    
        'zoomlevel':0,
        'action':'xhr.results.view.list',
        'page':page,
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

        return query
        

    def start_requests(self):
        for line in qc.Cities.strip().split('\n'):
            if line.find('#') == 0:
                continue

            for proptype in qc.Proptyes:
                for stat in qc.Statuses:
                    city, zipcode = line.split()
                    city = city.lower()
                    page = 1

                    query = self.gen_query( city, zipcode, proptype, stat, page ) 

                    url = Request('GET', Njmls.URL_LISTINGS, params = query, headers = Njmls.headers ).prepare().url

                    request =  scrapy.Request( url  ) 
                    request.meta['search_params'] = {
                    'city': city,
                    'zipcode': zipcode,
                    'proptype': proptype,
                    'stat': stat,
                    'page': page,
                    }
                    yield request

        
   
    def get_total_pages(self, response):
        
        n =  response.xpath('//div[@class="result-header"]//ol[@class="pagenumbers"]/li[@class="currentPage"]/text()').re('of (\d+)')[0]
        return int(n)

    def parse(self, response):

        pages = self.get_total_pages( response )
        self.logger.info('crawl params %s' % response.meta['search_params'] )
        self.logger.info('total page %s' % pages )

        
        for page in range(1, pages+1 ):
            search_params = response.meta['search_params'].copy()
            search_params['page'] = page
            query = self.gen_query( **search_params )

            houseData = HouseItem()
            houseData['town'] = search_params['city']
            houseData['state'] = 'nj'
            houseData['zipcode'] = search_params['zipcode']

            if search_params['proptype'] == qc.rental:
                houseData['type'] = 'rent'
            else:
                houseData['type'] = 'sell'

            url = Request('GET', Njmls.URL_LISTINGS, params = query, headers = Njmls.headers ).prepare().url

            request =  scrapy.Request( url, callback = self.parse_listing, dont_filter=True ) 
            request.meta['data'] = houseData
            request.meta['search_params'] = search_params
            yield request
        

    def parse_listing(self, response ):
        
        self.logger.info('parse listting: %s' % response.meta['search_params'])

        mlses = response.xpath('//div[@class]').re('houseresults listingrecord.*mls_number: \'(\d+)')

        for mls in mlses:
            
            query = {
            'action' : 'dsp.info',
            'mlsnum' :  mls,
            }

            houseData = response.meta['data'].copy()
            houseData['mls'] = mls

            url = Request('GET', Njmls.URL_LISTINGS, params = query, headers = Njmls.headers ).prepare().url
            request = scrapy.Request( url, callback =  self.parse_njmls_site )
            request.meta['data'] = houseData
            request.meta['search_params'] = response.meta['search_params']
            yield request

            

    

    def parse_njmls_site(self, response ):
        
        self.logger.info('crawl %s' % response.url )

        houseData = response.meta['data'].copy()
        isSold = response.meta['search_params'].stat == qc.sold
        
        houseRlt, mls_histories, image_links = self.extract_detail_page(response.body, isSold )
        houseData.update( houseRlt )

        houseData['images'] = image_links

        houseData['mlshistories'] = []
        for history in mls_histories: 
            
            data = MlsHistoryItem()
            data.update( history )
            houseData['mlshistories'].append( data )

        yield houseData



        
    def extract_detail_page(self, html, isSold):
        '''
        extract information for sell or rent
        isSold true, extract listing agent
        '''
        
        houseRlt={}
        soup = bs(html)
        listSection= soup.find('div', {'id': 'listsection'})
        if listSection:
            contents = listSection.findAll('strong')
            
            locale.setlocale(locale.LC_ALL, "")

            for content in contents:
                key= content.string.strip()
                value= normalize_text( content.nextSibling )


                if re.search(r'^Address', key):
                    houseRlt['address'] = value
            
                elif re.search(r'^Style', key):
                    houseRlt['style'] = value

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
        if features:
            features = features.findAll('strong')
            for f in features:
                key= f.string.strip()
                value = normalize_text ( f.nextSibling.nextSibling )

                if re.search(r'^Heat', key):
                    houseRlt['heatcool'] = value

                elif re.search(r'^Year', key):
                    p = re.search(r'(\d+)', value)
                    if p:
                        houseRlt['yearbuilt']= int(p.group(0))

                elif re.search(r'^Utilities', key):
                    houseRlt['utility'] = value

                elif re.search(r'^Provided', key):
                    houseRlt['provided'] = value

                elif re.search(r'^Pets',key):
                    houseRlt['pets'] = value
                    
                else:
                    pass
        
        # find listing agent if sold
        if isSold:
            agents = soup.find('div', {'class': 'nj-listing-agents' })
            if agents:
                agents = agents.findAll('strong') 
                for agent in agents:
                    key= agent.string.strip()
                    value = normalize_text ( agent.nextSibling )

                    if re.search(r'^Listing Agent', key):
                        tmp = {} 
                        try:
                            tmp['name'] = normalize_text( value.split(',')[0] )
                            tmp['tel']  = normalize_text( value.split(',')[1] )
                        except Exception:
                            pass
                
                        if tmp.has_key('name'):
                            houseRlt['listagent'] = tmp
        

        # find images 
        image_links = [ i.get('data-rsbigimg').replace('/h/', '/m/') for i in soup.findAll('a', {'class': 'rsImg'}) ]
        

        mls_history = []
        mls_prev = ''
        data = soup.find('div', {'class': "nj-grid-body nj-history-body" } )

        if data:
            for row in data.findAll('div', {'class': 'nj-row' }):
                mls = row.find('div', {'class': 'mls-num' } ).text.strip()
                if mls == '':
                    mls = mls_prev
                date = row.find('div', {'class': 'mls-date' } ).text.strip()
                price = row.find('div', {'class': 'mls-price' } ).text.strip()
                price = locale.atof(price.replace('$',''))
                status =  normalize_text ( row.find('div', {'class': 'mls-status' } ).text )
                mls_history.append({
                'mls': mls,
                'date': date,
                'price': price,
                'status': status
                })


                mls_prev = mls


        return (houseRlt, mls_history, image_links )
