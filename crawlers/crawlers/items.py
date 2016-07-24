# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from DB_models import House, Mlsinfo, Housemls, Mlshistory
import logging

Logger = logging.getlogger(__name__)

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
            House.create( address = self['address'],
                          state = self['state'],
                          town = self['town'],
                          zipcode = self['zipcode'],
                        ).save()
            Mlsinfo.create( mls = self['mls'], 
                            style = self.get('style', None ),
                        ).save()

        except KeyError as e:
            Logger.ERROR(e)
            

class MlsHistoryItem(scrapy.Item):
    mls = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()

    def update_data_base(self):
        print self['mls']
        pass
