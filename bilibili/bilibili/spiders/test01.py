# -*- coding: utf-8 -*-
import scrapy
import re
from bilibili.items import BilibiliItem
from copy import deepcopy
from selenium import webdriver
from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
chorme_options = Options()
chorme_options.add_argument("--headless")
chorme_options.add_argument("--disable-gpu")

class Test01Spider(scrapy.Spider):
    
    name = 'test01'
    allowed_domains = ['bilibili.com']
    # start_urls = ['https://www.bilibili.com/ranking/']
    target_count=5
    download_dir=r"F:\study_project\webpack\scrapy"
    webdriver_path=r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe'
    MAX_THREAD=5

    # 实例化一个浏览器对象
    def __init__(self):
        self.browser = webdriver.Chrome(self.webdriver_path,chrome_options=chorme_options)
        super().__init__()

    def start_requests(self):
        url ='https://www.bilibili.com/ranking/all/119/0/3' #"https://www.bilibili.com/ranking/"
        response = scrapy.Request(url,callback=self.parse)
        yield response

    def parse(self, response):
        ul=response.xpath('//li[@class="rank-item"]')
        video_meta=BilibiliItem()
        counts=0
        for li in ul:
            counts+=1
            if counts==self.target_count+1:
                break
            rank=li.xpath('./div[@class="num"]/text()').extract_first()
            img_url=li.xpath('./div[@class="content"]/div/a/div/img/@src').extract_first()
            name=li.xpath('./div[@class="content"]//img/@alt').extract_first()
            href=li.xpath('./div[@class="content"]/div[@class="info"]/a/@href').extract_first()

            view_counts=li.xpath('./div[@class="content"]//div[@class="detail"]/span[1]/text()').extract_first()
            review=li.xpath('./div[@class="content"]//div[@class="detail"]/span[2]/text()').extract_first()
            author=li.xpath('./div[@class="content"]//div[@class="detail"]/a/span/text()').extract_first()
            score=li.xpath('./div[@class="content"]//div[@class="pts"]/div/text()').extract_first()

            #|排名|缩略图|视频名|链接|播放量|评论量|分数|         未收集(发布时间、弹幕量、收藏量)，下面收集
            video_meta["rank"]=rank
            video_meta["img_url"]=img_url
            video_meta["name"]=name.strip()
            video_meta["href"]=href
            video_meta["aid"]=re.search(r'/av(\d+)/*', href).group(1)

            video_meta["view_counts"]=view_counts
            video_meta["review"]=review
            video_meta["author"]=author
            video_meta["score"]=score
            yield scrapy.Request(url=href,meta={'video_meta':deepcopy(video_meta)},callback=self.parse_detail)

    def parse_detail(self, response):
        video_meta=response.meta['video_meta']

        #|---发布时间---|---点赞---|---投币---|---收藏量---|---转发---|---弹幕量---|---分类---|

        pub_time=response.xpath('//*[@id="viewbox_report"]/div[1]/span[2]/text()').extract_first()
        like=response.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[1]/text()').extract_first()
        coins=response.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[2]/text()').extract_first()
        favorite=response.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[3]/text()').extract_first()

        forward=response.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[4]/text()').extract_first()
        barrage=response.xpath('//*[@id="viewbox_report"]/div[2]/span[2]/text()').extract_first()
        classes=response.xpath('//*[@id="viewbox_report"]/div[1]/span[1]/a[1]/text()').extract_first()

        ul=response.xpath('//ul[@class="tag-area clearfix"]/li')
        tags=[]
        for li in ul:
            tags.append(li.xpath('./a/text()').extract_first())

        video_meta["pub_time"]=pub_time
        video_meta["like"]=like
        video_meta["coins"]=coins.strip()
        video_meta["favorite"]=favorite
        video_meta["forward"]=forward
        video_meta["barrage"]=barrage
        video_meta["tags"]=tags
        video_meta["classes"]=classes
        video_meta["file_content"]="none"

        yield video_meta
            # yield{
            #     "rank":rank,
            #     "img_url":img_url,
            #     "name":name,
            #     "href":href,

            #     "view_counts":view_counts,
            #     "review":review,
            #     "author":author,
            #     "score":score
            # }
    # 整个爬虫结束后关闭浏览器
    def close(self,spider):
        self.browser.quit()


    