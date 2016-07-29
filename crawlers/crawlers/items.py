# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from DB_models import House, Mlsinfo, Housemls, Mlshistory, MlsImage
import logging
import peewee
import urllib

Logger = logging.getLogger(__name__)

class MlsHistoryItem(scrapy.Item):
    mls = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()

    def update_data_base(self):
        from datetime import datetime
        try:        
            mlshistory = Mlshistory.create( 
                            mls= self['mls'],
                            date = datetime.strptime( self['date'], '%m/%d/%Y').date(),
                            price = self.get('price', None ),
                            status = self.get('status', None ),
                            ) 

        except peewee.IntegrityError as e:
            pass 


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
    mlshistories = scrapy.Field()

    def update_data_base(self):

        house = House.get_or_create( 
                      address = self['address'],
                      state = self['state'],
                      town = self['town'],
                      defaults = { 'zipcode': self['zipcode']  }
                      )

        mls = Mlsinfo.get_or_create(  mls = self['mls'] )
            
        for attr in ( 
                    'style', 
                    'rooms', 
                    'bedrooms', 
                    'bathrooms',
                    'basement', 
                    'garage', 
                    'heatcool',
                    'utility',
                    'yearbuilt',
                    'tax', 
                    ):
            if mls.__getattribute__(attr) == None and self.get(attr, None) != None:
                # only update empty field    
                mls.__setattr__(attr, self.get(attr) )

        mls.save()
        
        try:
            Housemls.create_or_get(houseid = house, 
                                   mls = mls 
                                   )
        except peewee.IntegrityError as e:
            pass

        for link in self.get( 'images', [] ):
            try:
                mi = MlsImage.create( mls = mls,
                                      url = link,
                                    )
                mi.image =  urllib.urlopen( link ).read() 
                mi.save()
            except peewee.IntegrityError  as e:
                pass

            
            

        for mh in self.get('mlshistories', [] ):
            mh.update_data_base()
            
            
            try:
                Housemls.create(houseid = house, 
                                mls = mh['mls']
                                )
            except peewee.IntegrityError  as e:
                pass


