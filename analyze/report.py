import sys
sys.path.append('../dataBase')

from  DB_models import database, House, Agent, Mlsinfo, Housemls, Mlshistory
import datetime 
from peewee import *

def short_town(i):
    if i == 'east rutherford':
        return 'ERutherford'
    else:
        return i


def date_elpas(d1, d2):
    d1 = datetime.datetime.strptime(d1, '%Y-%m-%d').date()
    d2 = datetime.datetime.strptime(d2, '%Y-%m-%d').date()
    return (d1- d2).days

def print_mls():
    today = datetime.date.today()
    cut_date =  today - datetime.timedelta(days=150 ) 
    
    query =  ( Mlshistory.select(Mlshistory.mls, 
                                fn.Max(Mlshistory.date).alias('max_date'),
                                fn.Min(Mlshistory.date).alias('min_date') )
              .group_by(Mlshistory.mls)
              .order_by( SQL('max_date').desc() )
             )
            
    
    formatstr='{mls:8}|{type:5}|{date}|{onMarket:3}|{price:8}|{status:4}|{bedrooms:4}|{bathrooms:4}|{tax:>8}|{address:>35}|{town:>15}'

    for i in query:


        mlshist = ( Mlshistory.select().where( (Mlshistory.mls == i.mls_id) & 
                                               (Mlshistory.date == i.max_date) ))
        ii = mlshist[0]
        try:
            #print ii.mls.mls, ii.mls.type, ii.date, ii.price, ii.status, date_elpas(i.max_date, i.min_date )
            mlsinfo = ii.mls

            house = mlsinfo.house[0].house
            data={  
            'mls':   mlsinfo.mls,
            'type': mlsinfo.type,
            'date':  ii.date,  
            'onMarket': date_elpas( i.max_date, i.min_date),
            'price': ii.price, 
            'status': ''.join( [ _[0].upper() for _ in ii.status.split() ] ),
            'address': house.address,
            'town':  short_town(house.town),
            'bedrooms': mlsinfo.bedrooms,
            'bathrooms': mlsinfo.bathrooms,
            'tax': mlsinfo.tax
            }

            print formatstr.format(**data)

        except Mlsinfo.DoesNotExist : 
            pass
    

if __name__ == '__main__':
    print_mls()
    

