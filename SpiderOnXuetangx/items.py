# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    course_title = scrapy.Field()
    model = scrapy.Field()
    subject = scrapy.Field()
    teacher = scrapy.Field()
    teacher_from = scrapy.Field()
    teacher_subject = scrapy.Field()
    starttime = scrapy.Field()
    enrollment_sum = scrapy.Field()
    introduction = scrapy.Field()
    href = scrapy.Field()