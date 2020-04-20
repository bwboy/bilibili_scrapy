# -*- coding: utf-8 -*-
import scrapy
import re,json,logging,re,os
from baidu.items import BaiduItem
from selenium.common.exceptions import TimeoutException
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器
from baidu import settings
import urllib.parse

class MultipleSpider(scrapy.Spider):
    PROXIES_LIST=[] 
    # 单个视频的连接
    start_urls = ['http://v.baidu.com/watch/670898235286398193.html',
    'http://v.baidu.com/watch/6732132984955826029.html']
    # 最大线程
    MAX_THREADS=5

    name = 'multiple'
    allowed_domains = ['baidu.com']
    DOWNLOAD_DIR=settings.DOWNLOAD_DIR
    WEBDRIVER_PATH=settings.WEBDRIVER_PATH

    def __init__(self):
        # 装载代理
        self.getProxiesList()
        super().__init__()

    def parse(self, response):

        video_item=BaiduItem()

        title=response.xpath('//div[@class="title-cont"]/h2/text()').extract_first()
        author=response.xpath('//p[@class="title-info"]/span[@class="site"]/text()').extract_first()
        hot=response.xpath('//p[@class="title-info"]/span[@class="num play"]/text()').extract()
        update_time="" #response.xpath('//p[@class="title-info"]/span[@class="num play"]/text()').extract()
        stream_url=self.parse_html(response)


        video_item['title']=title
        video_item['name']="".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',title,re.S))
        video_item['author']=author
        video_item['hot']="".join(hot).strip()
        video_item['html_url']= response.url
        video_item['stream_url']=stream_url
        video_item['update_time']=update_time
        video_item["img_url"]=""

        yield video_item



    def parse_html(self,response):
        html=response.text
        start=html.find("videoFlashPlayUrl")+len("videoFlashPlayUrl = '")
        print(start)
        end=html.find("videoFlashPlayUrl",start)
        target_end=html.rfind("';",start,end)
        swf_url=html[start:target_end]
        start=swf_url.find("video=")+len("video=")
        stream_url=urllib.parse.unquote(swf_url[start:])
        return stream_url

    def getProxiesList(self):
        try:
            with open("proxy.txt","r",encoding="utf-8") as f:
                json_str=f.read()
            proxy_list=eval(json_str)
            [self.PROXIES_LIST.append(i) for i in proxy_list]
        except:
            print("不使用代理")