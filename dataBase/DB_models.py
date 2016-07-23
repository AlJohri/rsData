from peewee import *
import defs

database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database

class House(BaseModel):
    address = TextField()
    houseid = PrimaryKeyField(db_column='houseID')
    state = TextField()
    town = TextField()

    class Meta:
        db_table = 'house'
        indexes = (
            (('address', 'town', 'state'), True),
        )

class Mlsinfo(BaseModel):
    attic = TextField(null=True)
    basement = TextField(null=True)
    bathrooms = FloatField(null=True)
    bedrooms = FloatField(null=True)
    floodzone = IntegerField(null=True)
    floor = FloatField(null=True)
    garage = TextField(null=True)
    heatcool = TextField(null=True)
    images = BlobField(null=True)
    listrent = IntegerField(null=True)
    lot = FloatField(null=True)
    mls = PrimaryKeyField()
    rooms = FloatField(null=True)
    schoole = IntegerField(db_column='schoolE', null=True)
    schoolh = IntegerField(db_column='schoolH', null=True)
    schoolm = IntegerField(db_column='schoolM', null=True)
    style = TextField(null=True)
    tax = IntegerField(null=True)
    utility = TextField(null=True)
    yearbuilt = IntegerField(null=True)

    class Meta:
        db_table = 'mlsInfo'

class Housemls(BaseModel):
    houseid = ForeignKeyField(db_column='houseID', rel_model=House, to_field='houseid')
    mls = ForeignKeyField(db_column='mls', rel_model=Mlsinfo, to_field='mls')

    class Meta:
        db_table = 'houseMls'

class Mlshistory(BaseModel):
    date = DateField(null=True)
    mls = ForeignKeyField(db_column='mls', rel_model=Mlsinfo, to_field='mls')
    price = IntegerField(null=True)
    status = TextField(null=True)

    class Meta:
        db_table = 'mlshistory'

