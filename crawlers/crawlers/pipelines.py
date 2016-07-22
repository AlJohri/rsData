from DBAccessor import DBAccessor

class DataBasePipeline(object):
    def process_item(self, item, spider):
        item.update_data_base(db
