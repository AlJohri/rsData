from peewee import *
import defs

database = SqliteDatabase(defs.DBname)


class BaseModel(Model):
    class Meta:
        database = database

class House(BaseModel):
    '''
    house id to house location map
    '''
    houseid = PrimaryKeyField()
    address = FixedCharField()
    state = FixedCharField()
    town = FixedCharField()
    zipcode = FixedCharField(index=True)

    class Meta:
        indexes = (
            (('address', 'town', 'state'), True),
        )

class Mlsinfo(BaseModel):
    '''
    snapshot of all information for the mls.
    notice that for a location, the house can go through renovations,
    therefore, the mls the sole reference for the condition of the house that being sold 
    at the given time. 
    All relavent infomation are stored and should be enough to decide whether it is a good investment. 
    '''
    mls = FixedCharField( primary_key = True ) 
    attic = TextField(null=True)
    basement = TextField(null=True)
    bathrooms = FloatField(null=True)
    bedrooms = FloatField(null=True)
    floodzone = IntegerField(null=True)
    floor = FloatField(null=True)
    garage = TextField(null=True)
    heatcool = TextField(null=True)
    listrent = IntegerField(null=True)
    lot = FloatField(null=True)
    rooms = FloatField(null=True)
    schoole = IntegerField(null=True)
    schoolh = IntegerField(null=True)
    schoolm = IntegerField(null=True)
    style = TextField(null=True)
    tax = IntegerField(null=True)
    utility = TextField(null=True)
    yearbuilt = IntegerField(null=True)


class MlsImage(BaseModel):
    
    mls = ForeignKeyField(rel_model=Mlsinfo, to_field='mls', related_name='images' )
    url = CharField(unique=True)
    image = BlobField(null=True)


class Housemls(BaseModel):
    '''
    a house can be listed by multiple mlses
    '''
    houseid = ForeignKeyField(rel_model=House, to_field='houseid')
    mls = ForeignKeyField(rel_model=Mlsinfo, to_field='mls')

    class Meta:
        indexes = (
            (('houseid', 'mls'), True),
        )


class Mlshistory(BaseModel):
    '''
    a single mls can have multiple list status
    '''
    date = DateField()
    mls = ForeignKeyField(rel_model=Mlsinfo, to_field='mls')
    price = IntegerField(null=True)
    status = TextField(null=True)

    class Meta:
        indexes = (
            (('mls', 'date'), True),
        )
