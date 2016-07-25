import logging

Logger = logging.getLogger(__name__)

class DataBasePipeline(object):
    def process_item(self, item, spider):
        Logger.debug( item )
        item.update_data_base()
