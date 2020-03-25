# -*- coding: utf-8 -*-
import scrapy


class RankingspiderSpider(scrapy.Spider):
    name = 'rankingspider'
    allowed_domains = ['acfun.cn']
    start_urls = ['http://acfun.cn/']

    def parse(self, response):
        pass
