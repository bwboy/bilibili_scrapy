# -*- coding: utf-8 -*-
import scrapy
import re
from bilibili.items import BilibiliItem
from copy import deepcopy
from selenium import webdriver
from bilibili import settings
from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
chrome_options = Options()  #chrome
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

'''
爬取排行视频储存在本地。需要使用selenium打开每个页面。效率比较低，于是可以使用另一个。
'''
class Test01Spider(scrapy.Spider):
    
    name = 'test01'
    allowed_domains = ['bilibili.com']
    # start_urls = ['https://www.bilibili.com/ranking/']
    target_count=4
    LOGGING=[]
    download_dir=r"F:\study_project\webpack\scrapy"
    webdriver_path=r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe' #selenium驱动位置
    MAX_THREAD=5      #pipeline线程池
    VIDEO_QUALITY=16  #pipeline视频质量16 32 64 80 -> 360p 480p 720p 1080p
    TARGET_CLASS=1   #全站 动画 国创相关 音乐 舞蹈 游戏 科技 数码 生活 鬼畜 时尚 娱乐 影视

    # 实例化一个浏览器对象
    def __init__(self):
        try:
            self.check_param()
        except expression as e:
            self.LOGGING.append(e)
        self.browser = webdriver.Chrome(self.webdriver_path,chrome_options=chrome_options)
        self.browser.implicitly_wait(5)
        super().__init__()

    def start_requests(self):
        url ='https://www.bilibili.com/ranking/all/119/0/1' #"https://www.bilibili.com/ranking/"
        response = scrapy.Request(url,callback=self.parse)
        yield response

    #解析排行版页面信息。
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
            video_meta["avid"]='0'

            video_meta["view_counts"]=view_counts
            video_meta["review"]=review
            video_meta["author"]=author
            video_meta["score"]=score
            yield scrapy.Request(url=href,meta={'video_meta':deepcopy(video_meta)},callback=self.parse_detail)

    #进入的详情页av1234567抓取信息。
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
        if len(self.LOGGING)!=0:
            with open(self.download_dir + 'failed_log.log', "w+") as f:
                f.write(str(self.LOGGING))
            print("错误报告已经生成在:{}".format(self.download_dir+r'\failed_log.log'))

    def check_param(self):
        i11 =input('请填写目标个数（默认4个）：')
        i22 =input('请填最大线程数（默认5个）：')
        i33 =input('请填写视频质量（默认16：360p）：')
        i44 =input('请填写目标分类（默认1：全部）：')
        if(i11!=''):
            i1=int(i11)
            if(i1<=100):
                self.target_count=i1
                print("您选择了{}".format(self.target_count))

        if(i22!=''):
            i2=int(i22)
            if(i2<=20):
                self.MAX_THREAD=i2
                print("您选择了{}".format(self.MAX_THREAD))
        if(i33!=''):
            i3=int(i33)
            if(i3==16 or i3==32 or i3==64 or i3==80):
                self.VIDEO_QUALITY=i3
                print("您选择了{}".format(self.VIDEO_QUALITY))
        if(i44!=''):
            i4=int(i44)
            if( i4<=13 and i4>=1):
                self.TARGET_CLASS=i4
                print("您选择了{}".format(self.TARGET_CLASS))