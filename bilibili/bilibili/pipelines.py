# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pymysql import connect
import requests
import logging
logger=logging.getLogger()
import threading
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import os, time, re,random
import queue
from bilibili.settings import getMySQLConfig,getMongoConfig

# import random
# import imageio, urllib.request, sys
# from moviepy.editor import *
# imageio.plugins.ffmpeg.download()

class BilibiliPipeline(object):
    def process_item(self, item, spider):
        return item



class MysqlPipeline(object):
    def open_spider(self,spider):
        self.client=connect(
            host=getMySQLConfig()['host'],
            port=getMySQLConfig()['port'],
            user=getMySQLConfig()['user'],
            password=getMySQLConfig()['password'],
            db=getMySQLConfig()['db']
        )
        self.cursor=self.client.cursor()

    def process_item(self, item, spider):
        if spider.name!="userspider":
            args=[
                item["name"],
                int(item["rank"]),
                item["img_url"],
                item["href"],
                item["view_counts"],
                item["review"],
                item["author"],
                int(item["score"])
            ]
            args2=[
                # int(item["aid"]),
                item["name"],
                int(item["rank"]),
                item["img_url"],
                item["href"],
                item["view_counts"],
                item["review"],
                item["author"],
                int(item["score"]),

                item["pub_time"],
                item["like"],
                item["coins"],
                item["favorite"],
                item["forward"],
                item["barrage"],
                str(item["tags"]),
                item["classes"],
                item["file_content"],
                item["avid"],
                item["cid"],
            ]
            # sql='insert into bilibili_rank VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s)'
            sql2='insert into bilibili_info VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            # self.cursor.execute(sql,args)
            self.cursor.execute(sql2,args2)
        else:
            args2=[
                # int(item["aid"]),
                item["title"],
                int(0),
                item["img_url"],
                "---",
                item["view"],
                item["reply"],
                item["author"],
                int(0),

                item["pub_time"],
                item["like"],
                item["coins"],
                item["favorite"],
                item["forward"],
                item["barrage"],
                str(item["tags"]),
                item["classes"],
                item["file_content"],
                item["avid"],
                item["cid"],
            ]

            sql2='insert into bilibili_info VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql2,args2)

        

        self.client.commit()
        return item


    def close_spider(self,spider):
        self.cursor.close()
        self.client.close()


class RankingPipeline(object):
    threads_list=[]
    DOWNLOAD_RETRY=[]
    LOGGING=queue.Queue()
    SUCCESS_QUEUE=queue.Queue()
    executer=None
    PROXIES_LIST=[]
    doneCount=0
    lock=threading.Lock()
    def open_spider(self,spider):
        self.executer=ThreadPoolExecutor(spider.MAX_THREAD)
        self.PROXIES_LIST=spider.PROXIES_LIST

    def handle_error(self,e):
        print("出错啦！")
        print(e)

    def close_spider(self,spider):

        wait(self.threads_list, return_when=ALL_COMPLETED)
        if len(self.PROXIES_LIST)==0 and spider.EnableProxy==True:
            [self.LOGGING.put(i) for i in self.DOWNLOAD_RETRY]
            raise RuntimeError("没有可用的代理了。下载结束！")

        self.executer.shutdown()
        print("共有{}个文件下载失败。".format(len(self.DOWNLOAD_RETRY)))
        print("共有{}个文件被下载。".format(self.SUCCESS_QUEUE.qsize()))
        #错误报告导出
        if self.LOGGING.qsize()!=0:
            with open(spider.download_dir + 'failed_log.log', "w+") as f:
                f.write(json.dumps([self.LOGGING.get() for i in range(1,self.LOGGING.qsize())]))
                f.close()
            print("错误报告已经生成在:{}".format(spider.download_dir+r'\failed_log.log'))

    def process_item(self, item, spider):
        headers={
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Range': 'bytes=0-',  # Range 的值要为 bytes=0- 才能下载完整视频
                'Referer': 'https://api.bilibili.com/x/web-interface/view?aid=' + str(item['avid']),  # 注意修改referer,必须要加的!
                'Origin': 'https://www.bilibili.com',
                'Connection': 'keep-alive',
        }
        detail_url='https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn={}'.format(item['cid'], item["avid"], spider.VIDEO_QUALITY)
        jsonp=requests.get(url=detail_url,headers=headers).json()
        video_list=[]
        for video_item in jsonp['data']['durl']:
            video_list.append(video_item['url'])
        if not os.path.exists(os.path.join(spider.download_dir, 'bilibili_video', item['title'])):
            os.mkdir(os.path.join(spider.download_dir, 'bilibili_video', item['title']))
        item["file_content"]=str(os.path.join(spider.download_dir, 'bilibili_video', item['title']))
        img_name=os.path.join(spider.download_dir, 'bilibili_video', item['title'],'{}'.format(item['img_url'].split('/')[-1]))
        img=self.executer.submit(self.download_img,item["img_url"],img_name)
        self.threads_list.append(img)

        if item['pages']>1:
            count=1
            for video_url in video_list:
                filename=os.path.join(spider.download_dir, 'bilibili_video', item['title'],'{}-{}.flv'.format(item['part'],count))
                video_download=self.executer.submit(self.download_video,video_url, filename, headers=headers)
                self.threads_list.append(video_download)
                count+=1
        else:
            for video_url in video_list:
                filename=os.path.join(spider.download_dir, 'bilibili_video', item['title'],'{}.flv'.format(item['title']))
                video_download=self.executer.submit(self.download_video,video_url, filename, headers=headers)
                self.threads_list.append(video_download)
        return item

    def download_img(self,img_url,filename):
        response_img=requests.get(url=img_url,verify=False,stream=True)
        with open(filename,'wb+') as f:
            f.write(response_img.content)
        print("【图片下载完成】：{}".format(filename))

    def download_video(self,url,filename,headers):
        
        self.SUCCESS_QUEUE.put({"url":url,"filename":filename,"headers":headers})
        proxy=None
        response_stream=None
        if len(self.PROXIES_LIST)!=0:
            proxy=random.choice(self.PROXIES_LIST)
        if proxy!=None:
            response_stream=requests.get(url=url,headers=headers,verify=False,stream=True,proxies=proxy)
            if response_stream.status_code!=200:
                print("【代理出现错误：{}】".format(proxy))
                self.download_retry(filename,url,headers)
        else:
            response_stream=requests.get(url=url,headers=headers,verify=False,stream=True)
        print("【视频下载开始】：{}---proxy:{}".format(filename,proxy))
        f = open(filename,'wb+')
        for chunk in response_stream.iter_content(chunk_size=10240):
            if chunk:
                f.write(chunk)
        f.close()
        
    def download_retry(self,filename,url,headers):
        count=0
        while True:
            response_stream=requests.get(url=url,headers=headers,verify=False,stream=True,proxies=random.choice(self.PROXIES_LIST))
            if response_stream.status_code==200:
                print("【重试成功，下载开始】：{}---proxy:{}".format(filename,proxy))
                f = open(filename,'wb+')
                for chunk in response_stream.iter_content(chunk_size=10240):
                    if chunk:
                        f.write(chunk)
                f.close()
                break
            count+=1
            if count==5:
                print("【重试失败】：{}".format(filename))
                break


        

'''test01专用pipeline，没事别用'''
class DownloadVideoPipeline(object):
    
    def open_spider(self,spider):
        
        self.executer=ThreadPoolExecutor(spider.MAX_THREAD)

    def close_spider(self,spider):
        wait(self.threads_list, return_when=ALL_COMPLETED)
        self.executer.shutdown()

    def process_item(self, item, spider):
        if spider.name!='test01':
            return item
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        bvid=item['href'].split('/')[-1]
        item['bvid']=bvid
        res_cid=requests.get('https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(bvid),headers=headers).json()
        cid_list=[]
        for cid in res_cid['data']:
            cid_list.append(cid['cid'])
        cid=cid_list[0]
        item['cid']=cid
        res_aid=requests.get('https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}'.format(cid,bvid),headers=headers).json()
        aid =res_aid['data']['aid']
        item['avid']=aid
        self.download_path=spider.download_dir
        start = str(item['avid'])
        start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + str(item['avid'])
        quality =spider.VIDEO_QUALITY    #input('请填写116或112或80或74或64或32或16:')
        html = res_aid #requests.get(start_url, headers=headers).json()
        data = html['data']
        cid_list = []
        if '?p=' in start:
            # 单独下载分P视频中的一集
            p = re.search(r'\?p=(\d+)', start).group(1)
            cid_list.append(data['pages'][int(p) - 1])
        else:
            # 如果p不存在就是全集下载
            cid_list = data['pages']
        item["img_url"]=data['pic'].split('@')[0]
        for obj_item in cid_list:
            cid = str(obj_item['cid'])
            title=item["name"]
            print('[下载视频的cid]:' + cid)
            print('[下载视频的标题]:' + title)
            page = str(obj_item['page'])
            start_url = start_url + "/?p=" + page
            video_list = self.get_play_list(aid,cid,quality)
            start_time = time.time()
            if not os.path.exists(os.path.join(self.download_path, 'bilibili_video', title)):
                #开启线程，提交任务。
                #t=self.executer.submit(self.down_video,video_list, title, start_url, page)
                print("-------------------开始下载图片-------------------------")
                try:
                    img=self.executer.submit(self.download_img,item["img_url"],title)
                    self.threads_list.append(img)
                    video_download=self.executer.submit(self.download_video,video_list, title, start_url, page)
                    item["file_content"]=str(os.path.join(self.download_path, 'bilibili_video', title))
                    self.threads_list.append(video_download)
                except:
                    self.LOGGING.put(e)
                    self.LOGGING.put({
                        'title':title,
                        'url':start_url
                    })

            else:
                print("文件已存在！直接跳过！")
                item["file_content"]=os.path.join(self.download_path, 'bilibili_video', title)
            #self.down_video(video_list, title, start_url, page)
        return item

    # 访问API地址
    def get_play_list(self,aid, cid, quality):
        url_api = 'https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn={}'.format(cid, aid, quality)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Cookie': 'SESSDATA=aa15d6af%2C1560734457%2Ccc8ca251', # 登录B站后复制一下cookie中的SESSDATA字段,有效期1个月
            'Host': 'api.bilibili.com'
        }
        html = requests.get(url_api, headers=headers).json()
        video_list = []
        for i in html['data']['durl']:
            video_list.append(i['url'])
        print(video_list)
        return video_list

    def download_img(self,img_url,title):
        currentVideoPath = os.path.join(self.download_path, 'bilibili_video', title)
        response_img=requests.get(url=img_url,verify=False,stream=True)
        filename=os.path.join(currentVideoPath, r'{}'.format(img_url.split('/')[-1]))
        with open(filename,'wb+') as f:
            f.write(response_img.content)

    def download_video(self,video_list, title, start_url, page):
        num=1
        print('[正在下载P{}段视频,请稍等...]:'.format(page) + title)
        currentVideoPath = os.path.join(self.download_path, 'bilibili_video', title)  # 当前目录作为下载目录
        headers={
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Range': 'bytes=0-',  # Range 的值要为 bytes=0- 才能下载完整视频
                'Referer': start_url,  # 注意修改referer,必须要加的!
                'Origin': 'https://www.bilibili.com',
                'Connection': 'keep-alive',
        }
        for video_url in video_list:
            if not os.path.exists(currentVideoPath):
                os.makedirs(currentVideoPath)
            # 开始下载
            response_stream=requests.get(url=video_url,headers=headers,verify=False,stream=True)
            filename=os.path.join(currentVideoPath, r'{}.flv'.format(title)) # 写成mp4也行  title + '-' + num + '.flv'

            if len(video_list) > 1:
                filename=os.path.join(currentVideoPath, r'{}-{}.flv'.format(title, num).format(download_dir,video_title,video_title))
            f = open(filename,'wb+')
            for chunk in response_stream.iter_content(chunk_size=10240):# 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
                if chunk:
                    f.write(chunk)
            f.close()
            num += 1

''' 开启将数据储存到mongo '''
class MongoPipeline(object):
    def open_spider(self,spider):
        url = getMongoConfig()
        self.client=MongoClient(url)

    def process_item(self, item, spider):
        self.client.bilibili.video.insert_one(item)
        return item

    def close_spider(self,spider):
        self.client.close()