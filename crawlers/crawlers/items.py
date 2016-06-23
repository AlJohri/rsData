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

class MlsHistoryItem(scrapy.Item):
    mls = scrapy.Item()
    data = scrapy.Item()
    price = scrapy.Item()
    status = scrapy.Item()
