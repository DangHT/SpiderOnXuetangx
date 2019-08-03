# -*- coding: utf-8 -*-
import scrapy

from SpiderOnXuetangx.items import CourseItem


class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['www.xuetangx.com']
    start_urls = ['http://www.xuetangx.com/courses']

    courses_url = 'http://www.xuetangx.com/courses?credential=0&page_type=0&cid=0&process=0&org=0&course_mode=0&page={page}'

    page = 1    # 记录当前页数
    id = 1

    def start_requests(self):
        yield scrapy.Request(self.courses_url.format(page=self.page), self.parse)

    def parse(self, response):
        courses = response.css('#list_style > li')
        for course in courses:
            item = CourseItem()
            course_title = course.css('div > div.fl.list_inner_right.cf > div > a > h2::text').extract_first()
            model = course.css('div > div.fl.list_inner_right.cf > div > div.coursename_ref > span.model::text').extract_first()
            # 注意! 学科类型可以是多种融合
            subject = course.css('div > div.fl.list_inner_right.cf > div > div.coursename_ref > span.subject > a::text').extract()
            teacher = course.css('div > div.fl.list_inner_right.cf > div > div.cf.teacher > div.fl.name > ul > li:nth-child(1) > span:nth-child(1)::text').extract_first()
            teacher_from = course.css('div > div.fl.list_inner_right.cf > div > div.cf.teacher > div.fl.name > ul > li:nth-child(1) > span:nth-child(2)::text').extract_first()
            teacher_subject = course.css('div > div.fl.list_inner_right.cf > div > div.cf.teacher > div.fl.name > ul > li:nth-child(1) > span:nth-child(3)::text').extract_first()
            starttime = course.css('div > div.fl.list_inner_right.cf > div > div.cf.teacher > div.fl.name > ul > li:nth-child(2) > span::text').extract_first()
            enrollment_sum = course.css('div > div.fl.list_inner_right.cf > div > div.cf.teacher > div.fl.name > ul > li:nth-child(3) > span::text').extract_first()
            introduction = course.css('div > div.fl.list_inner_right.cf > div > div.txt_all > p.txt::text').extract_first()
            image = 'http://www.xuetangx.com' + course.css('div > div.img.fl > a > img::attr(src)').extract_first()
            if introduction is None:
                introduction = course.css('div > div.fl.list_inner_right.cf > div > div.txt_all > p.ktxt::text').extract_first()
            href = response.urljoin(course.css('div > div.fl.list_inner_right.cf > div > a::attr(href)').extract_first())
            item['course_title'] = course_title
            if model is not None:
                item['model'] = ''.join(list(filter(str.isalnum, model))) # 删除多余字符
            item['subject'] = subject
            item['teacher'] = teacher
            item['teacher_from'] = teacher_from
            item['teacher_subject'] = teacher_subject
            item['starttime'] = starttime
            item['enrollment_sum'] = enrollment_sum
            if introduction is not None:
                item['introduction'] = ''.join(list(filter(str.isalnum, introduction)))
            item['href'] = href
            item['image'] = image
            item['course_id'] = self.id
            self.id += 1
            yield item

        self.page += 1

        if not response.css('body > div.search_page > article > div > div.no_data_search'):
            yield scrapy.Request(url=self.courses_url.format(page=self.page), callback=self.parse)

