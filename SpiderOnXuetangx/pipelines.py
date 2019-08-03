# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import csv
import os
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

class ToCsvPipeline(object):

    def __init__(self):
        #csv文件位置，无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/course.csv'
        #打开（创建）文件
        self.file = open(store_file, 'w', encoding="utf-8", newline='')
        #csv写入
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        if item['course_id'] is not None:
            subject = ""
            if item['subject'] is not None:
                for s in item['subject']:
                    s += "|"
                    subject += s
            if item['teacher'] is None:
                teacher = "null"
            else:
                teacher = item['teacher']
            if item['teacher_from'] is None:
                teacher_from = "null"
            else:
                teacher_from = item['teacher_from']
            if subject is None or subject == "":
                subject = "null"
            if item['introduction'] is None:
                introduction = "null "
            else:
                introduction = item['introduction']
            self.writer.writerow((item['course_id'], item['course_title'], teacher, teacher_from, subject[:-1], introduction, item['href'], item['image']))
        return item

    def close_spider(self, spider):
        self.file.close()