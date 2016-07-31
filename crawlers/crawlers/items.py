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
from scrapy.exceptions import DropItem

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
                            date = datetime.strptime( self['date'], '%m/%d/%y').date(),
                            price = self.get('price', None ),
                            status = self.get('status', None ),
                            ) 

        except (peewee.IntegrityError, KeyError) as e:
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
        
        houseError= False
        try:
            house, _created = House.get_or_create( 
                          address = self['address'],
                          state = self['state'],
                          town = self['town'],
                          defaults = { 'zipcode': self['zipcode']  }
                          )
        except KeyError as e:
            houseError = True

        mls, _created = Mlsinfo.get_or_create(  mls = self['mls'] )
        
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
            if mls.__getattribute__(attr) == None  and  self.get(attr, None ) != None:
                mls.__setattr__(attr, self.get(attr) )
        
        mls.save()
        

        for link in self.get( 'images', [] ):
            mi, created = MlsImage.get_or_create( mls = mls,
                                  url = link,
                                )
            if created:
                try:
                    mi.image = urllib.urlopen( link ).read() 
                    mi.save()
                except Exception as e:
                    pass
        
        if not houseError:
            try:
                Housemls.create(houseid = house, 
                                       mls = mls 
                                       )
            except peewee.IntegrityError as e:
                pass
            

        for mh in self.get('mlshistories', [] ):
            mh.update_data_base()
            
            
            if not houseError:
                try:
                    Housemls.create(houseid = house, 
                                    mls = mh['mls']
                                    )
                except peewee.IntegrityError  as e:
                    pass


