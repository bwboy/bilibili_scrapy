# -*- coding: utf-8 -*-
import scrapy,re,json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器
from bilibili.items import VideoInfoItem
from copy import deepcopy
from bilibili import settings
import logging
logger=logging.getLogger()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"')


class RankingspiderSpider(scrapy.Spider):
    name = 'rankingspider'
    allowed_domains = ['bilibili.com']
    URL='https://www.bilibili.com/ranking/'
    download_dir=settings.getDownloadDir()
    webdriver_path=settings.getWebDriverPath()
    target_count=4
    MAX_THREAD=5
    VIDEO_QUALITY=16  #pipeline视频质量16 32 64 80 -> 360p 480p 720p 1080p
    TARGET_CLASS=6   #全站 动画 国创相关 音乐 舞蹈 游戏 科技 数码 生活 鬼畜 时尚 娱乐 影视
    PROXIES_LIST=[] #[{"http":"117.94.213.117:8118"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"}]

    # 实例化一个浏览器对象
    def __init__(self):
        try:
            self.check_param()
        except expression as e:
            logger.warning("输入参数有误，已返回默认值。")
        self.LOGGING=[]
        self.EnableProxy=False
        self.browser = webdriver.Chrome(self.webdriver_path,chrome_options=chrome_options)
        self.browser.implicitly_wait(10)
        super().__init__()

    def start_requests(self):
        yield scrapy.Request(self.URL,callback=self.parse)

    def parse(self, response):
        self.getProxiesList() # 装载代理
        logger.warning("------------爬虫正式开始！----代理个数：{}------------".format(len(self.PROXIES_LIST)))
        ul=response.xpath('//li[@class="rank-item"]')
        video_meta=VideoInfoItem()
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
            video_meta["bvid"]=href.split('/')[-1]
            detail_url='https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(video_meta["bvid"])

            print("----------------{}-------------------".format(counts))
            # yield video_meta
            yield scrapy.Request(url=detail_url,meta={'video_meta':deepcopy(video_meta)},callback=self.parse_cid)

    def parse_cid(self,response):
        video_meta=response.meta['video_meta']
        jsonp=json.loads(response.text)
        video_meta['cid']=jsonp['data'][0]['cid']
        logger.warning("---------------{}---------------------".format(video_meta['cid']))
        detail_url='https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}'.format(video_meta['cid'],video_meta['bvid'])
        yield scrapy.Request(url=detail_url,meta={'video_meta':video_meta},callback=self.parse_detail)
        
    def parse_detail(self,response):
        video_meta=response.meta['video_meta']
        jsonp=json.loads(response.text)
        data=jsonp['data']
        video_meta['avid']=data['aid']
        video_meta["img_url"]=data['pic']
        #|---发布时间---|---点赞---|---投币---|---收藏量---|---转发---|---弹幕量---|---播放次数---|---回复数---|---标签---|---分类---|
        video_meta["pub_time"]=data['pubdate']
        video_meta["like"]=data['stat']['like']
        video_meta["coins"]=data['stat']['coin']
        video_meta["favorite"]=data['stat']['favorite']
        video_meta["forward"]=data['stat']['share']
        video_meta["barrage"]=data['stat']['danmaku']
        video_meta["view"]=data['stat']['view']
        video_meta["reply"]=data['stat']['reply']
        video_meta["tags"]=data['dynamic']
        video_meta["classes"]=data['tname']
        video_meta["file_content"]="none"
        video_meta["pages_list"]=data['pages']
        video_meta["title"]=data['title']
        for video_item in video_meta['pages_list']:
            video_meta["pages"]=len(video_meta['pages_list'])
            video_meta["cid"]=video_item['cid']
            video_meta["part"]=video_item['part']
            yield video_meta

    # 整个爬虫结束后关闭浏览器
    def close(self,spider):
        self.browser.quit()
        print("爬虫已关闭！")

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

    def getProxiesList(self):
        try:
            with open("proxy.txt","r",encoding="utf-8") as f:
                json_str=f.read()
            proxy_list=eval(json_str)
            [self.PROXIES_LIST.append(i) for i in proxy_list]
        except:
            print("不使用代理")
        
        