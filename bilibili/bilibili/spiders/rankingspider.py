# -*- coding: utf-8 -*-
import scrapy


class RankingspiderSpider(scrapy.Spider):
    name = 'rankingspider'
    allowed_domains = ['bilibili.com']
    start_urls = ['http://bilibili.com/']

    def parse(self, response):
        pass
