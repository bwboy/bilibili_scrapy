# -*- coding: utf-8 -*-
import scrapy


class UserspiderSpider(scrapy.Spider):
    name = 'userspider'
    allowed_domains = ['bilibili.com']
    start_urls = ['http://bilibili.com/']

    def parse(self, response):
        pass
