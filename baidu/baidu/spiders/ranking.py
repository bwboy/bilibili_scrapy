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

class RankingSpider(scrapy.Spider):


    # 单个视频的连接 - 默然搞笑分组
    start_urls = ['http://v.baidu.com/channel/short/newamuse'] 
    # 最大线程
    MAX_THREADS=5
    # 下载个数
    COUNT=3
    # 代理列表
    PROXIES_LIST=[] 
    name = 'ranking'
    allowed_domains = ['baidu.com']
    DOWNLOAD_DIR=settings.DOWNLOAD_DIR
    WEBDRIVER_PATH=settings.WEBDRIVER_PATH

    def __init__(self):
        # 填写并检查初始化参数
        # try:
        #     self.check_param()
        # except:
        #     logger.warning("输入参数有误，已返回默认值。")
        self.getProxiesList() # 装载代理
        self.start_urls[0]+='?callback=jQuery111104289298378003823_1586930112490&format=json'
        # self.browser = webdriver.Chrome(self.WEBDRIVER_PATH,chrome_options=chrome_options)
        # self.browser.implicitly_wait(5)
        super().__init__()

    def parse(self, response):
        video_item=BaiduItem()
        start=response.text.find("(")+1
        end=response.text.rfind(")")
        json_str=response.text[start:end]
        json_callback=json.loads(json_str)
        videos=json_callback['data']['videos']
        current_count=0
        for item in videos:
            video_item['title']=item['title']
            video_item['name']="".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',item['title'],re.S))
            video_item['update_time']=item['update_time']
            video_item['html_url']= item['url']
            video_item['img_url']= item['imgv_url']
            video_item['stream_url']=self.parse_stream_url(item['play_link'])
            # if item['play_link']=="":
                # yield scrapy.Request(url=video_item['html_url'],meta={'video_item':deepcopy(video_item)},callback=self.parse_detail)
            # yield video_item
            yield scrapy.Request(url=video_item['html_url'],meta={'video_item':deepcopy(video_item)},callback=self.parse_detail)
            current_count+=1
            if current_count==self.COUNT:
                break

    def parse_detail(self,response):

        video_item=response.meta['video_item']
        title=response.xpath('//div[@class="title-cont"]/h2/text()').extract_first()
        author=response.xpath('//p[@class="title-info"]/span[@class="site"]/text()').extract_first()
        hot=response.xpath('//p[@class="title-info"]/span[@class="num play"]/text()').extract()
        stream_url=self.parse_html(response)

        video_item['title']=title
        video_item['name']="".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',title,re.S))
        video_item['author']=author
        video_item['hot']="".join(hot)
        video_item['stream_url']=stream_url

        yield video_item



    def parse_html(self,response):
        html=response.text
        start=html.find("videoFlashPlayUrl")+len("videoFlashPlayUrl = '")
        print(start)
        end=html.find("videoFlashPlayUrl",start)
        target_end=html.rfind("';",start,end)
        swf_url=html[start:target_end]
        return self.parse_stream_url(swf_url)

    def parse_stream_url(self,swf_url):
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