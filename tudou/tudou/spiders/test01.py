# -*- coding: utf-8 -*-
import scrapy
import re,json,logging,re,os
from tudou.items import TudouItem
from selenium.common.exceptions import TimeoutException
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器
from tudou import settings

# 初始化全局配置。
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# 针对Linux环境下的chrome driver参数
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# 不使用图片
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs",prefs)


chrome_options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"')
logger=logging.getLogger()


class Test01Spider(scrapy.Spider):
    # 爬取多少个视频
    COUNT=5
    # 排行榜(分类位置)
    start_urls = ['https://www.tudou.com/sec/622336449?spm=a2h28.8313461.top.dtab']
    # 最大线程
    MAX_THREADS=5

    name = 'test01'
    allowed_domains = ['tudou.com','youku.com']
    DOWNLOAD_DIR=settings.DOWNLOAD_DIR
    WEBDRIVER_PATH=settings.WEBDRIVER_PATH
    def __init__(self):
        # 填写并检查初始化参数
        try:
            self.check_param()
        except:
            logger.warning("输入参数有误，已返回默认值。")
        self.browser = webdriver.Chrome(self.WEBDRIVER_PATH,chrome_options=chrome_options)
        self.browser.implicitly_wait(5)
        super().__init__()

    def parse(self, response):
        video_meta=TudouItem()
        div=response.xpath('//div[@data-spm="feed"]/a[1]')
        target=0
        for a in div:
            url=a.xpath('./@href').extract()
            title=a.xpath('./@title').extract()
            img_src=a.xpath('./div[1]/img/@src').extract()
            video_meta['title']= title
            video_meta['pageurl']="http:"+"".join(url)
            video_meta['img_src']=''.join(img_src)
            yield scrapy.Request(url=video_meta['pageurl'],meta={'video_meta':deepcopy(video_meta)},callback=self.parse_detail)
            target+=1
            if target == self.COUNT:
                break

    def parse_detail(self,response):
        video_meta=response.meta['video_meta']
        url_list=response.xpath('//html/head/script/@src')
        headers={
            "Referer": video_meta['pageurl'],
            "Sec-Fetch-Mode": "no-cors",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        for item in url_list:
            url="".join(item.extract())
            if "get.json" in url:
                video_meta['callback']=url
                yield scrapy.Request(headers=headers,url=video_meta['callback'],meta={'video_meta':video_meta},callback=self.parse_callback)
                break

    def parse_callback(self,response):
        video_meta=response.meta['video_meta']
        data_text=response.text                 #  bytes.decode(res.content)
        start= data_text.find("(")+1
        end=data_text.rfind(")")
        data_str=data_text[start:end]
        data=json.loads(data_str)['data']
        video_meta['name']="".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',data['video']['title'],re.S)) #data['video']['title']
        stream=data['stream']
        mp4_list=[]
        for item in stream:
            download_url=item['segs'][0]['cdn_url']
            mp4_list.append(download_url)
            print(download_url)
        print(mp4_list[-1])
        video_meta['stream_url']=mp4_list[-1]
        yield video_meta

    def close(self,spider):
        if self.browser!=None:
            self.browser.quit()
        print("爬虫已关闭！")


    def check_param(self):
        target_url =input('请填写排行榜分类地址（默认音乐分类）：')
        current_count =input('请填下载个数（默认4个）：')
        current_thread =input('请填最大线程数（默认5）：')
        if(target_url!=''):
            self.start_urls[0]=target_url
            print("1.您选择了{}".format(self.start_urls))

        if(current_thread!=''):
            i2=int(current_thread)
            if(i2<=20):
                self.MAX_THREADS=i2
                print("2.您选择了{}".format(self.MAX_THREADS))

        if(current_count!=''):
            i2=int(current_count)
            if(i2<=20):
                self.COUNT=i2
                print("3.您选择了{}".format(self.COUNT))
