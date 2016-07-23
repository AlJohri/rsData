# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

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

    def update_data_base(self, db ):
        print self['mls']
        pass

class MlsHistoryItem(scrapy.Item):
    mls = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()

    def update_data_base(self, db ):
        print self['mls']
        pass
