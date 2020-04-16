# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    hot = scrapy.Field()
    file_content = scrapy.Field()
    tag = scrapy.Field()
    stream_url = scrapy.Field()

    update_time=scrapy.Field()
    img_url=scrapy.Field()
    html_url=scrapy.Field()
    
