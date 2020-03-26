# -*- coding: utf-8 -*-
import scrapy
import re,json,logging,re,os
from bilibili.items import UserVideoInfoItem
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器

from bilibili import settings
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"')

logger=logging.getLogger()


class UserspiderSpider(scrapy.Spider):
    name = 'userspider'
    allowed_domains = ['bilibili.com']
    # 下载视频列表。有多少个都放进去。
    start_urls = ['https://www.bilibili.com/video/BV1ob411p7oc']
    # start_urls = ['https://www.bilibili.com/video/BV1d7411m78N',
    # 'https://www.bilibili.com/video/BV1kE411P7gx',
    # 'https://www.bilibili.com/video/BV1PE411W78K',
    # 'https://www.bilibili.com/video/BV1k7411T7RH']
    download_dir=settings.getDownloadDir()
    webdriver_path=settings.getWebDriverPath()
    MAX_THREAD=5
    # 填写b站用户空间或用户id，爬取他的全部视频,不开启请填写None。target_count是爬取个数,默认4个。填写这里之后不再执行start_urls里内容。
    userId=None#'https://space.bilibili.com/883968/video' #None
    target_count=5
    # 其他参数
    VIDEO_QUALITY=16  #pipeline视频质量16 32 64 80 -> 360p 480p 720p 1080p
    PROXIES_LIST=[] #[{"http":"117.94.213.117:8118"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"}]



    def __init__(self):
        # try:
        #     self.check_param()
        # except expression as e:
        #     logger.warning("输入参数有误，已返回默认值。")
        self.browser=None
        self.LOGGING=[]
        self.EnableProxy=False
        super().__init__()

    def parse(self, response):
        self.getProxiesList() #装载代理
        video_meta=UserVideoInfoItem()
        if self.userId!=None:
            self.browser = webdriver.Chrome(self.webdriver_path,chrome_options=chrome_options)
            self.browser.implicitly_wait(10)
            userid=re.search(r'/(\d+)/*', self.userId).group(1)
            if not userid:
                raise RuntimeError("用户不存在。")
            url='https://space.bilibili.com/{}/video'.format(userid)
            yield scrapy.Request(url=url,meta={'video_meta':video_meta},callback=self.parse_space)
        else:
            for url in self.start_urls:
                video_meta["bvid"]=url.split('/')[-1]
                detail_url='https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(video_meta["bvid"])
                yield scrapy.Request(url=detail_url,meta={'video_meta':deepcopy(video_meta)},callback=self.parse_cid)

    def parse_space(self,response):
        video_meta=response.meta['video_meta']
        ul=response.xpath('//*[@id="submit-video-list"]/ul[2]/li')
        count=0
        for li in ul:
            video_meta["bvid"]=li.xpath('./a[1]/@href').extract_first().split('/')[-1]
            detail_url='https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(video_meta["bvid"])
            yield scrapy.Request(url=detail_url,meta={'video_meta':deepcopy(video_meta)},callback=self.parse_cid)
            count+=1
            if count==self.target_count:
                break

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
        video_meta["file_content"]=None
        video_meta["pages_list"]=data['pages']
        video_meta["title"]=data['title']
        video_meta['author']=data["owner"]['name']
        for video_item in video_meta['pages_list']:
            video_meta["pages"]=len(video_meta['pages_list'])
            video_meta["cid"]=video_item['cid']
            video_meta["part"]=video_item['part']
            yield video_meta


    def close(self,spider):
        if self.browser!=None:
            self.browser.quit()
        print("爬虫已关闭！")



    def getProxiesList(self):
        try:
            with open("proxy.txt","r",encoding="utf-8") as f:
                json_str=f.read()
            proxy_list=eval(json_str)
            [self.PROXIES_LIST.append(i) for i in proxy_list]
        except:
            print("不使用代理")
