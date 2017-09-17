#!/usr/bin/env python
import sys
from collections import defaultdict, namedtuple
import numpy as np
import datetime

RentRecord = namedtuple('RentRecord', 'price  post_date days_on_market')

def parseTable( lines ):
    '''
    return { area: { bed : [price, ... ] }  }
    '''

    namedtuple

    type_idx =1 
    list_date_idx = 2
    date_on_mark = 3
    price_idx=4
    stat_idx =5
    bed_idx  =6
    area_idx =10

    

    data = [ map( lambda x: x.strip(), line.strip().split('|') ) for line in lines if line.strip() != '' ]
    data = [  i for i in data if i[type_idx] == 'rent'  ]

    rental_stat = defaultdict( lambda: defaultdict(list) )

    to_date = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date()

    for i in data:
        record = RentRecord( float( i[price_idx] ), 
                             to_date( i[list_date_idx] ), 
                             int( i[date_on_mark]  )
                           )

        rental_stat[ i[area_idx] ][ int( float( i[bed_idx] )) ].append( record )

    return rental_stat
    

def genStat( table ):
    
    rawData = table 
    
    stat = defaultdict( lambda: defaultdict(dict) )
    for area, v in rawData.items():
        for bed, records in v.items(): 
            prices = [  r.price for r in records ]
            donM = [ r.days_on_market for r in records  ]
            stat[area][bed]['median'] = np.median( prices )
            stat[area][bed]['25'] = np.percentile( prices, 25 )
            stat[area][bed]['75'] = np.percentile( prices, 75 )
            stat[area][bed]['num'] = len( prices ) 
            stat[area][bed]['donm'] = int(np.mean( donM ) )

    return stat


def printPriceStat( rental_stat ):
    
    formatstr = '{:20}{:>5}{:>8}{:>8}{:>8}{:>8}{:>8}'
    print formatstr.format( 'area', 'bed', 'num', '25', 'median', '75', 'donm' )
    

    for area, v in rental_stat.items():
        total_number = 0 
        for bed, stat in v.items():
            print formatstr.format( area, bed, stat['num'], 
                                    stat['25'], stat['median'], stat['75'],
                                    stat['donm'],
                                  )          
            total_number += stat['num']
        
        print 
        print 'total_number: %s' % total_number 
        print 

def printCityStat( table ):
    
    formatstr = '{:20}{:>8}{:>8}'
    
    print formatstr.format( 'city', 'total', 'days' )
    for area, v in table.items():
        
        records = [ j   for i in  v.values() for j in i  ]
        print formatstr.format( area,  len(records ) , 0 )


def main():
        
    data = open( sys.argv[1] ).readlines()  
    table = parseTable( data )
    
    rental_stat = genStat( table ) 

    printPriceStat( rental_stat )
    printCityStat( table )



if __name__ == '__main__':
    
    main()
