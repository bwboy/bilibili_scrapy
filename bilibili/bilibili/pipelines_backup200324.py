# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pymysql import connect

import requests, time, urllib.request, re
from moviepy.editor import *
import os, sys
# import imageio

import threading
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import random
# imageio.plugins.ffmpeg.download()

class BilibiliPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def open_spider(self,spider):
        self.client=connect(
            host='127.0.0.1',
            port=3306,
            user='wxwmodder',
            password='sxmc321',
            db='scrapy01'
        )
        self.cursor=self.client.cursor()

    def process_item(self, item, spider):
        # if item[file_content]:
        #     print("文件已存在，数据库不再写入。")
        #     return
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


        sql='insert into bilibili_rank VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s)'

        sql2='insert into bilibili_info VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql,args)
        self.cursor.execute(sql2,args2)
        self.client.commit()
        return item


    def close_spider(self,spider):
        self.cursor.close()
        self.client.close()


class DownloadVideoPipeline(object):
    
    def open_spider(self,spider):
        self.threads_list=[]
        self.executer=ThreadPoolExecutor(spider.MAX_THREAD)

    def close_spider(self,spider):
        wait(self.threads_list, return_when=ALL_COMPLETED)
        self.executer.shutdown()


    def process_item(self, item, spider):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        '''
        res_aid=requests.get('https://api.bilibili.com/x/player/pagelist?bvid={BV14E411W7od}&jsonp=jsonp'.format(bvid))
        res_videolist-requests.get('https://api.bilibili.com/x/web-interface/view?cid=160387688&bvid=BV14E411W7od'.format())
        '''
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
        # if start.isdigit() == True:
        #     # 如果输入的是av号
        #     # 获取cid的api, 传入aid即可
        #     aid = start
        #     start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + aid
        # else:
        #     # 如果输入的是url (eg: https://www.bilibili.com/video/av46958874/)
        #     aid = re.search(r'/av(\d+)/*', start).group(1)
        #     start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + aid

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
                except expression as e:
                    spider.LOGGING.append(e)
                    spider.LOGGING.append({
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
        print("-------------------开始下载图片{}-------------------------".format(title))
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


    # @Deprecated  :不再使用urllib，使用requests全部搞定。
    #  下载图片
    def down_img(self,img_url,title):
        currentVideoPath = os.path.join(self.download_path, 'bilibili_video', title)
        opener = urllib.request.build_opener()
        opener.addheaders = [
                # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
                ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
                ('Accept', '*/*'),
            ]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url=img_url, filename=os.path.join(currentVideoPath, r'{}'.format(img_url.split('/')[-1])))
    # @Deprecated  :不再使用urllib，使用requests全部搞定。
    #  下载视频
    def down_video(self,video_list, title, start_url, page):
        num = 1
        print('[正在下载P{}段视频,请稍等...]:'.format(page) + title)
        currentVideoPath = os.path.join(self.download_path, 'bilibili_video', title)  # 当前目录作为下载目录
        for i in video_list:
            opener = urllib.request.build_opener()
            # 请求头
            opener.addheaders = [
                # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
                ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
                ('Accept', '*/*'),
                ('Accept-Language', 'en-US,en;q=0.5'),
                ('Accept-Encoding', 'gzip, deflate, br'),
                ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
                ('Referer', start_url),  # 注意修改referer,必须要加的!
                ('Origin', 'https://www.bilibili.com'),
                ('Connection', 'keep-alive'),
            ]
            urllib.request.install_opener(opener)
            # 创建文件夹存放下载的视频
            if not os.path.exists(currentVideoPath):
                os.makedirs(currentVideoPath)
            # 开始下载
            if len(video_list) > 1:
                urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}-{}.flv'.format(title, num))
                                        )  # 写成mp4也行  title + '-' + num + '.flv'
            else:
                urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}.flv'.format(title))
                                        )  # 写成mp4也行  title + '-' + num + '.flv'
            num += 1
        self.combine_video(video_list, title)

    # 合并视频  可能也不再用moviepy.editor库中的文件。
    # @Deprecated
    def combine_video(self,video_list, title):
        currentVideoPath = os.path.join(sys.path[0], 'bilibili_video', title)  # 当前目录作为下载目录
        if len(video_list) >= 2:
            # 视频大于一段才要合并
            print('[下载完成,正在合并视频...]:' + title)
            # 定义一个数组
            L = []
            # 访问 video 文件夹 (假设视频都放在这里面)
            root_dir = currentVideoPath
            # 遍历所有文件
            for file in sorted(os.listdir(root_dir), key=lambda x: int(x[x.rindex("-") + 1:x.rindex(".")])):
                # 如果后缀名为 .mp4/.flv
                if os.path.splitext(file)[1] == '.flv':
                    # 拼接成完整路径
                    filePath = os.path.join(root_dir, file)
                    # 载入视频
                    video = VideoFileClip(filePath)
                    # 添加到数组
                    L.append(video)
            # 拼接视频
            final_clip = concatenate_videoclips(L)
            # 生成目标视频文件
            final_clip.to_videofile(os.path.join(root_dir, r'{}.mp4'.format(title)), fps=24, remove_temp=False)
            print('[视频合并完成]' + title)

        else:
            # 视频只有一段则直接打印下载完成
            print('[视频合并完成]:' + title)


    def Schedule_cmd(self,blocknum, blocksize, totalsize):
        speed = (blocknum * blocksize) / (time.time() - start_time)
        # speed_str = " Speed: %.2f" % speed
        speed_str = " Speed: %s" % self.format_size(speed)
        recv_size = blocknum * blocksize

        # 设置下载进度条
        f = sys.stdout
        pervent = recv_size / totalsize
        percent_str = "%.2f%%" % (pervent * 100)
        n = round(pervent * 50)
        s = ('#' * n).ljust(50, '-')
        f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
        f.flush()
        # time.sleep(0.1)
        f.write('\r')
    # 字节bytes转化K\M\G
    def format_size(self,bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            print("传入的字节格式不对")
            return "Error"
        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%.3fG" % (G)
            else:
                return "%.3fM" % (M)
        else:
            return "%.3fK" % (kb)




class MongoPipeline(object):
    def open_spider(self,spider):
        url = 'mongodb://root:root@127.0.0.1:27017/admin'
        self.client=MongoClient(url)

    def process_item(self, item, spider):
        self.client.bilibili.video.insert_one(item)
        return item

    def close_spider(self,spider):
        self.client.close()