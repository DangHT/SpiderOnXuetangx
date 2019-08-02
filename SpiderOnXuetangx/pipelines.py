# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

#仅保留课程简介中不大于limit的文字
class IntroPipeline(object):

    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['introduction']:
            if len(item['introduction']) > self.limit:
                item['introduction'] = item['introduction'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')

class MongoPipeline(object):

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        # 无学科分类信息的课程暂存于‘no_subject’数据库中
        if len(item['subject']) > 0:
            for subject in item['subject']:
                # 将学科名翻译为中文, 并作为数据库的名称
                self.db[subject].update({'course_title': item['course_title']}, {'$set': item}, True)
        else:
            self.db['no_subject'].update({'course_title': item['course_title']}, {'$set': item}, True)
        return item

    def close_spider(self, spider):
        self.client.close()