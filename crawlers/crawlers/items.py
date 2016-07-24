# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from DB_models import House, Mlsinfo, Housemls, Mlshistory
import logging
import peewee

Logger = logging.getLogger(__name__)

class HouseItem(scrapy.Item):
    mls  = scrapy.Field()
    address = scrapy.Field()
    town = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    style = scrapy.Field()
    rooms = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    basement = scrapy.Field()
    garage = scrapy.Field()
    heatcool = scrapy.Field()
    utility = scrapy.Field()
    yearbuilt = scrapy.Field()
    tax = scrapy.Field()
    images = scrapy.Field()

    def update_data_base(self):
        try:
            house = House.create( address = self['address'],
                          state = self['state'],
                          town = self['town'],
                          zipcode = self['zipcode'],
                        )
            mls = Mlsinfo.create( mls = self['mls'] )
            
            housemls = Housemls.create(houseid = house, 
                                       mls = mls 
                                      )


        except (KeyError, peewee.IntegrityError ) as e:
            Logger.ERROR(e)
        
        Mlsinfo.update( style       = self.get('style', None ),
                        rooms       = self.get('rooms', None ),
                        bedrooms    = self.get('bedrooms', None ),
                        bathrooms   = self.get('bathrooms', None ),
                        basement    = self.get('basement', None ),
                        garage      = self.get('garage', None ),
                        heatcool    = self.get('heatcool', None ),
                        utility     = self.get('utility', None ),
                        yearbuilt   = self.get('yearbuilt', None ),
                        tax         = self.get('tax', None ),
                     ).where( Mlsinfo.mls == self['mls'] )
            

class MlsHistoryItem(scrapy.Item):
    mls = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()

    def update_data_base(self):
        try:        
            mlshistory = Mlshistory.create( **self ) 

        except peewee.IntegrityError as e:
            Logger.ERROR(e)
                                        
