# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TudouItem(scrapy.Item):
    # define the fields for your item here like:
    # 文件名
    name = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 页面的url
    pageurl=scrapy.Field()
    # 包含流的jsonp
    callback=scrapy.Field()
    # 流地址
    stream_url=scrapy.Field()
    # 缩略图地址
    img_src=scrapy.Field()

    # 回复数
    reply=scrapy.Field()
    # 作者
    author=scrapy.Field()
    # 上传时间
    update_time=scrapy.Field()
    # 文件目录
    file_content=scrapy.Field()


# class TudouItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
