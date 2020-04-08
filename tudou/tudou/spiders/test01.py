# -*- coding: utf-8 -*-
import scrapy


class Test01Spider(scrapy.Spider):
    name = 'test01'
    allowed_domains = ['tudou.com']
    start_urls = ['http://tudou.com/']

    def parse(self, response):
        pass
