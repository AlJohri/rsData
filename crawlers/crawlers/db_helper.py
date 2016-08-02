from  DB_models import database, House, Agent, Mlsinfo, Housemls, Mlshistory

def get_next_dummy_address():
     
    hs= House.select().where(House.address.startswith('nxstd') )
    
    names = [ i.address for i in hs ]
    
    if names:
        nums = [ int(i.split('-')[1]) for i in names  ]
        return '%s-%d' % ('nxstd', max(nums) + 1 )
    
    else:
        return 'nxstd-1'
