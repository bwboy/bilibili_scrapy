# -*- coding: utf-8 -*-
import scrapy,re,json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器
from bilibili.items import VideoInfoItem
from copy import deepcopy
import logging
logger=logging.getLogger()
chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"')


class RankingspiderSpider(scrapy.Spider):
    name = 'rankingspider'
    allowed_domains = ['bilibili.com']

    URL='https://www.bilibili.com/ranking/'
    webdriver_path=r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe'
    download_dir=r"F:\study_project\webpack\scrapy"
    target_count=4
    MAX_THREAD=5
    VIDEO_QUALITY=16  #pipeline视频质量16 32 64 80 -> 360p 480p 720p 1080p
    TARGET_CLASS=3   #全站 动画 国创相关 音乐 舞蹈 游戏 科技 数码 生活 鬼畜 时尚 娱乐 影视
    LOGGING=[]



    # 实例化一个浏览器对象
    def __init__(self):
        # try:
        #     self.check_param()
        # except expression as e:
        #     self.LOGGING.append(e)
        self.browser = webdriver.Chrome(self.webdriver_path,chrome_options=chrome_options)
        self.browser.implicitly_wait(10)
        super().__init__()

    def start_requests(self):
        url='https://www.bilibili.com/ranking/'

        yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        print("---------------------爬虫正式开始！--------------------------------")
        ul=response.xpath('//li[@class="rank-item"]')
        print("----------------{}-------------------".format(1))
        print("-----------UL长度-----{}-------------------".format(len(ul)))
        video_meta=VideoInfoItem()
        print("----------------{}-------------------".format(2))
        counts=0
        for li in ul:
            print("----------------{}-------------------".format(3))
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

        # print(response.text)
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


            #detail_url='https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn={}'.format(video_item['cid'], video_meta["avid"], self.VIDEO_QUALITY)
        yield video_meta
    
    #         yield scrapy.Request(url=detail_url,meta={'video_meta':deepcopy(video_meta)},callback=self.parse_video)

    # def parse_video(self,response):
    #     jsonp=response.json()
    #     data=jsonp['data']


    # 整个爬虫结束后关闭浏览器
    def close(self,spider):
        self.browser.quit()
        if len(self.LOGGING)!=0:
            print()
            with open(self.download_dir + 'failed_log.log', "w+") as f:
                f.write(json.dumps(self.LOGGING))
                f.close()
            print("错误报告已经生成在:{}".format(self.download_dir+r'\failed_log.log'))
        print("爬虫已关闭！")
