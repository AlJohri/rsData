from DBAccessor import DBAccessor

class DataBasePipeline(object):
    def process_item(self, item, spider):
        with DBAccessor() as db:
            item.update_data_base(db)
