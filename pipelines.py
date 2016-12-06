# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
#from pymongo import MongoClient

#=============================================================
# Default pipeline (returns item)

class EdgeCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

#=============================================================
# Removes articles with duplicate doi

class DuplicatesPipeline (object):

    def __init__(self):
        self.dois_seen = set()

    def process_item(self, item, spider):
        if item ['doi'] in self.dois_seen:
            raise DropItem ("Duplicate item found: %s" % item)
        else:
            self.dois_seen.add (item ['doi'])
            return item

#=============================================================
# Writes article item to json

class JsonWriterPipeline (object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps (dict (item)) + "\n"
        self.file.write (line)
        return item

#=============================================================
# Store items in PyMongo DB

#class PyMongoDBPipeline (object):
#
#    collection_name = 'Articles'
#
#    def __init__(self, mongo_uri, mongo_db):
#        self.mongo_uri = mongo_uri
#        self.mongo_db  = mongo_db
#
#    @classmethod
#    def from_crawler(cls, crawler):
#        return cls(
#            mongo_uri = crawler.settings.get ('MONGO_URI'),
#            mongo_db  = crawler.settings.get ('MONGO_DATABASE', 'EdgeCrawler')
#        )
#
#    def open_spider(self, spider):
#        self.client = pymongo.MongoClient (self.mongo_uri)
#        self.db = self.client [self.mongo_db]
#
#    def close_spider(self, spider):
#        self.client.close()
#
#    def process_item(self, item, spider):
#        self.db [self.collection_name].insert (dict (item))
#        return item
