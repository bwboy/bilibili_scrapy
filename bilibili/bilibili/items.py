# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    rank = scrapy.Field()
    img_url = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    view_counts = scrapy.Field()
    review = scrapy.Field()
    author = scrapy.Field()
    score = scrapy.Field()

    pub_time = scrapy.Field()
    like = scrapy.Field()
    coins = scrapy.Field()
    favorite = scrapy.Field()
    forward = scrapy.Field()
    barrage = scrapy.Field()
    tags = scrapy.Field()
    classes = scrapy.Field()


    aid = scrapy.Field()
