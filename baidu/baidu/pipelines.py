# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED

from pymongo import MongoClient
from pymysql import connect
from baidu import settings
import requests
import logging
logger=logging.getLogger()
import threading
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import os, time, re,random

lock=Lock()

class BaiduPipeline(object):
    def process_item(self, item, spider):
        return item


class RankingPipeline(object):
    logfile=None
    threads_list=[]
    executer=None
    
    def open_spider(self,spider):
        self.executer=ThreadPoolExecutor(spider.MAX_THREADS)
        self.PROXIES_LIST=spider.PROXIES_LIST
        self.logfile = open("LOGGING.log","a+",encoding="utf-8")
        self.write_logging("{}:----------主线程开始-------------".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))

    def handle_error(self,e):
        self.write_logging("{}:pipeline出现错误".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))


    def process_item(self, item, spider):
        video_download=self.executer.submit(self.download_mp4,item['stream_url'],spider.DOWNLOAD_DIR,item['name'])
        self.threads_list.append(video_download)
        self.write_logging("{}:视频下载开始:{}/{}/{}.mp4".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),spider.DOWNLOAD_DIR,item['name'],item['name']))
        return item

    def download_mp4(self,video_url,download_dir,video_title):
        proxy=None
        response_stream=None
        if len(self.PROXIES_LIST)!=0:
            proxy=random.choice(self.PROXIES_LIST)
        if proxy!=None:
            response_stream=requests.get(url=url,headers=headers,verify=False,stream=True,proxies=proxy)
            if response_stream.status_code!=200:
                print("【代理出现错误：{}】".format(proxy))
                self.write_logging("{}:【代理出现错误：{}】".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),proxy))
                self.download_retry("{0}/{1}/{2}.mp4".format(download_dir,video_title,video_title),video_url)
        else:
            response_stream=requests.get(url=video_url,verify=False,stream=True)
        if not os.path.exists(download_dir+'/{}'.format(video_title)):
            os.makedirs(download_dir+'/{}'.format(video_title))
        f = open("{0}/{1}/{2}.mp4".format(download_dir,video_title,video_title),'wb+')
        for chunk in response_stream.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        f.close()
        print("视频下载完成:{}".format("{0}/{1}/{2}.mp4".format(download_dir,video_title,video_title)))
        self.write_logging("{0}:视频下载完成:{1}/{2}/{3}.mp4".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),download_dir,video_title,video_title))


    # 重试下载函数
    def download_retry(self,filename,url):
        count=0
        while True:
            response_stream=requests.get(url=url,verify=False,stream=True,proxies=random.choice(self.PROXIES_LIST))
            if response_stream.status_code==200:
                print("【重试成功，下载开始】：{}---proxy:{}".format(filename,proxy))
                self.write_logging("{}:【重试成功，下载开始】：{}---proxy:{}".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),filename,proxy))
                f = open(filename,'wb+')
                for chunk in response_stream.iter_content(chunk_size=10240):
                    if chunk:
                        f.write(chunk)
                f.close()
                break
            count+=1
            if count==5:
                print("【重试失败】：{}".format(filename))
                self.write_logging("{}:【重试失败】：{}".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),filename))
                break

    def close_spider(self,spider):
        print("pipeline退出")
        wait(self.threads_list, return_when=ALL_COMPLETED)
        self.write_logging("{}:----------爬虫结束-------------".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
        self.logfile.close()
        # with open("LOGGING.log","a+",encoding="utf-8") as f:
        #     for item in RankingPipeline.LOGGING:
        #         f.write("{}\r\n".format(item))
        
    def write_logging(self,text):
        lock.acquire()
        # with open("LOGGING.log","a+",encoding="utf-8") as f:
        self.logfile.write("{}\r\n".format(text))
        lock.release()




'''
当启用mysql时每条数据蒋经过此类处理。
'''
class MysqlPipeline(object):
    def open_spider(self,spider):
        self.client=connect(
            host=settings.MYSQL_CONFIG['host'],
            port=settings.MYSQL_CONFIG['port'],
            user=settings.MYSQL_CONFIG['user'],
            password=settings.MYSQL_CONFIG['password'],
            db=settings.MYSQL_CONFIG['db']
        )
        self.cursor=self.client.cursor()

    def process_item(self, item, spider):

        args=[
            item["name"],
            item["title"],
            item["img_src"],
            item["stream_url"],
        ]
        sql2='insert into baidu_info VALUES(0,%s,%s,%s,%s)'
        self.client.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.client.close()


''' 开启将数据储存到mongo '''
class MongoPipeline(object):
    def open_spider(self,spider):
        url = settings.MONGO_CONFIG
        self.client=MongoClient(url)

    def process_item(self, item, spider):
        self.client.baidu.video.insert_one(item)
        return item

    def close_spider(self,spider):
        self.client.close()