@[TOC](Bilibili爬虫url分析) 
# 项目总体说明 
+ `test01.py`第一个爬虫，用于手动爬取排行榜，性能比较低
+ `rankingspider.py` 爬取排行榜，只访问排行榜第一个页面，剩下数据全部由接口抓取。比上一个稍有提升。
+ `userspider.py`用户投稿全部爬取。
+ `forwordspider.py`收藏夹爬取。 


## 文件`rankingspider.py`架构。
+ 简单说明，之后再详细说明。
1. 请求交给`SeleniumInterceptMiddleware`，由selenium打开目标url，爬取排行榜信息。
2. 此时浏览器挂机，`scrapy`爬取api接口获得视频`aid` `cid` `bid`和`metadata`。
3. 将`VideoInfoItem`交给`RankingPipeline`，解析视频地址列表。
4. 从视频列表向线程池提交下载任务。
5. 爬虫结束后关闭selenium保存错误日志。 

## 文件`test01.py`架构。
+ 简单说明，之后再详细说明。
1. 请求交给`SeleniumInterceptMiddleware`，由selenium打开目标，爬取排行榜信息。
2. 再由selenium进入详情页，爬取详细信息。
3. 将item交给`DownloadVideoPipeline`，爬取视频，生成路径和图片信息。
4. 再将item交给`MysqlPipeline`，写入数据库。
5. 爬虫结束后关闭selenium保存错误日志。

# URL 分析 2020/3/23 
**【重要】**:这天bilibili改了url规则，直接导致下面逻辑不可用。
+ 简介：由`bvid`获取`cid`，再由`cid`和`bvid`获取`aid`，再由`aid`和`cid`获取`视频流url`。
## 1. 获取cid 
+
	```python
	res_cid=requests.get('https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(bvid),headers=headers_list).json()
	cid_list=[]
	for cid in res_cid['data']:
	    cid_list.append(cid['cid'])
	cid=cid_list[0]
	```
## 2. 通过cid - bvid 获取aid 
+	
	```python
	res_aid=requests.get('https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}'.format(cid,bvid),headers=headers_list).json()
	aid =res_aid['data']['aid']
	```
## 3. 通过 aid cid 获取视频列表文件 
+ 
	```python
	url_api = 'https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn={}'.format(cid, aid, quality)
	```
+ **注意:** 若看不懂，请看下面在看上面。了解如何`演变`而来。

# URL分析 @Desprecated
## 1. 获取cid
+ 每个视频有av号，例如av12345678，我们需要拿出其中的`数字`。访问到如下地址，获取视频`cid`。这个url不仅可以获取cid并且能够获取`封面地址`、`title`和`视频分P`一些其他信息。`想要得到视频流地址，必须先获得视频cid`
	```python
	start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + aid
	```
## 2. 获取资源url列表 
+ `aid`和`cid`有了我们就可以携带信息访问如下url地址，来获取视频视频的下载连接的url地址。`quality`是视频质量：`1080p60:116`;`1080p+:112`;`1080p:80`;`720p60:74`;`720p:64`;`480p:32`;`360p:16`; **注意**:1080p+,1080p60,720p60,720p都需要带入大会员的`cookie`中的`SESSDATA`才行,普通用户的`SESSDATA`最多只能下载`1080p`的视频。
	```python
	url_api = 'https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn={}'.format(cid, aid, quality)
	```
+ 但是访问上面的url时，携带如下的header：登录B站后复制一下`cookie`中的`SESSDATA`字段,有效期1个月，这样就可以下载更清晰的视频。
	```python
	headers = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	    'Cookie': 'SESSDATA=aa15d6af%2C1560734457%2Ccc8ca251', # 登录B站后复制一下cookie中的SESSDATA字段,有效期1个月
	    'Host': 'api.bilibili.com'
	}
	```
## 3. 得到视频流地址。 
+ 通过访问上面的url，就可以得到视频流的url列表了。例如访问
`https://api.bilibili.com/x/player/playurl?cid=120570181&avid=69542806&qn=112`
就可以在`response.data.durl[0].url`里获得视频流`下载链接`，而且还可以看到以下json：
	```json
	{
		"backup_rul": ["http://upos-sz-mirrorkodo.bilivideo.com/xxx",
			"http://upos-sz-mirrorkodo.bilivideo.com/xxx",
			"http://upos-sz-mirrorkodo.bilivideo.com/xxx",
		]
	}
	```
+ 上面的应该是备份信息，我们不去管他。我的得到的`response.data.durl`应该是个列表，每个列表中都包含`url`如果视频流地址。我们通过他下载就可以了。
+ 访问视频流地址时候需要携带如下`header` ，大家注意到，header里有个`start_url`，要填写上文中的`start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + aid`，也就是`第一步获取cid`时候的url。
	```python
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
	```

# bilibili_scrapy 
## bilibili爬虫实验室 


## 启动说明
1. 请安装依赖模块： 
`pip install -r requirements.txt`
2. 在pipeline中修改配置好的数据库连接，在附录中有表结构： 
```python
self.client=connect(
            host='127.0.0.1',
            port=3306,
            user='wxwmodder',
            password='sxmc321',
            db='scrapy01'
        )
```
3. 在`test01.py`修改参数:
    + 下载文件保存路径`download_dir=r"F:\study_project\webpack\scrapy\bilibili\bilibili\spiders"` 
    + 下载多少个`target_count=2` 
    + Chrome浏览器驱动路径`webdriver_path=r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe'`
    + 配置下载线程数：`MAX_THREAD=5`

4. 切换到`../bilibili_scrapy/bilibili`目录下：
    + `scrapy crawl test01`
## 附录
+ 附录表结构：
```Mysql
CREATE TABLE `bilibili_rank` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `img_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `href` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `view_counts` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `review` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `author` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=259 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE `bilibili_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `img_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `href` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `view_counts` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `review` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `author` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `pub_time` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `like` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `coins` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `favorite` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Forward` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `barrage` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tags` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `classes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `file_content` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
      `avid` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cid` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=224 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```