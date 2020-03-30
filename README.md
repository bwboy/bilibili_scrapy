
@[TOC](Bilibili爬虫url分析) 
# 项目总体说明 
## 特性 
bilibili视频爬取工具。可以自定义支持`线程池`、`Mysql`、`Mongo`、`设置代理`。支持从`排行榜`爬取、从`用户投稿空间`爬取、和`单个、多个视频`爬取和`分P`爬取、缩略图爬取和元信息(metadata)爬取,元信息可以看数据库表结构。
+ `userspider.py`用户投稿全部爬取。
+ `rankingspider.py` 爬取排行榜。
+ `test01.py`测试用，用于手动爬取排行榜，性能比较低不推荐使用。
# 快速开始
1. 克隆或拉取项目后，请安装依赖模块： 
`pip install -r requirements.txt`

2. 设置下载目录，打开"`bilibili_scrapy/bilibili/bilibili/settings.py`"
	```python
	# 下载目录
	DOWNLOAD_DIR=r"F:\study_project\webpack\scrapy"
	# chrome驱动路径（快速开始请忽略，排行榜必须设置这一项）
	WEBDRIVER_PATH=r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe'
	```
3. 切换到目录"`bilibili_scrapy/bilibili/`"
	```cmd
	scrapy crawl userspider
	```
4. 此时就可以看到你所设置的目录中文件了。 
# 配置说明
## 爬虫`userspider`，自定义爬取和用户投稿爬取
+ **多个视频:** 刚才的例子中，我们使用了userspider爬取了一个视频。若要自己添加多个视频。可以打开"`bilibili_scrapy/bilibili/bilibili/spider/userspider.py`"
	```python
		#目标地址。
	    start_urls = ['https://www.bilibili.com/video/BV1ob411p7oc']
	    #如果有多个地址，可以这样写。
	    start_urls = ['https://www.bilibili.com/video/BV1d7411m78N',
	     'https://www.bilibili.com/video/BV1kE411P7gx',
	     'https://www.bilibili.com/video/BV1PE411W78K',
	     'https://www.bilibili.com/video/BV1k7411T7RH']
	```
+ 其他爬虫初始配置`线程数`、`用户投稿爬取`、`视频质量`、`代理设置`。
	```python
		# 线程数量。
	    MAX_THREAD=5
	    # 填写b站用户空间或用户id，爬取他的全部视频,不开启请填写None。target_count是爬取个数,默认4个。填写这里之后不再执行start_urls里内容。
	    userId=None#'https://space.bilibili.com/883968/video'
	    target_count=5
	    # 其他参数
	    VIDEO_QUALITY=16  #pipeline视频质量16 32 64 80 -> 360p 480p 720p 1080p
	    PROXIES_LIST=[] #代理格式：[{"http":"117.94.213.117:8118"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"}]
	```
+ 爬取用户投稿。
1. 确定配置了chrome的驱动程序，上文`settings.py`提到。
2. `userId`填写空间地址，或者用户id。注意当`userId`有值时，不在爬取`start_urls`里的内容。
3. 设置一下爬取数量和线程。因为有些用户投稿的视频，很多。。
4. 仍然执行`scrapy crawl userspider`
## 爬虫`rankingspider`，排行榜爬取。 
基本上参数配置和上面差不多。但是这里支持参数热传入。直接执行。`确保你设置了chrome驱动路径。`
```cmd
scrapy crawl rankingspider
```
根据提示输入参数即可。
## 开启中间件及Mysql Mongo配置说明。
+ 元数据存入Mysql的基本配置。数据库表在最下面的附录中。
1. 打开`settings.py`配置mysql、Mongo数据库连接配置：
	```python
	#mysql配置
	MYSQL_CONFIG={"host":'127.0.0.1',
	            "port":3306,
	            "user":'wxwmodder',
	            "password":'sxmc321',
	            "db":'scrapy01'}
	#Mongo配置
	MONGO_CONFIG='mongodb://root:root@127.0.0.1:27017/admin'
	```
2. 开启mysql或mongo的Pipeline，仍然是`settings.py`，开启请取消注释，关闭打开注释。注意未配置的情况下不要开启pipline。
	```python
	ITEM_PIPELINES = {
	   'bilibili.pipelines.RankingPipeline':302,   #下载pipeline
	   'bilibili.pipelines.MysqlPipeline':350,	#mysqlpipeline
	   # 'bilibili.pipelines.MongoPipeline':352,  #mongo
	}
	```
## 代理中间件使用。
+ 自定义代理列表。爬虫中都包含了，可自定义配置代理列表。**注意**，*当代理列表不为空时，下载将随机使用代理，如果出错将在代理列表中重新选择，如果重试5次仍然失败则跳过。*如果为空。将不使用代理。
	```python
	PROXIES_LIST=[] 
	#[{"http":"117.94.213.117:8118"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"}]
	```
+ 自动获取代理，目前还是"试用中的功能"，注意开启了这个功能后。如果没有代理被加载则抛出异常。*原则上不使用本地代理下载*
	```python
	DOWNLOADER_MIDDLEWARES = {
	#代理中间件
	   # 'bilibili.middlewares.ProxyHandlerMiddleware': 1,
	   'bilibili.middlewares.SeleniumInterceptMiddleware': 2,
	}
	```
## 其他插件
+ 在 unittest目录中有个文件`proxytest.py`可以用来爬取可用代理。和一些单元测试，和项目无关。

## 目录结构  
+ |-- bilibili_scrapy   
    |-- datereport.md   
    |-- README.md			说明  
    |-- requirements.txt	依赖  
    |-- acfun				acfun爬虫测试  
    |-- bilibili			bilibili爬虫项目  
        |-- scrapy.cfg		scrapy配置文件  
        |-- bilibili		bilibili爬虫目录  
            |-- items.py	爬取视频的元信息metadata  
            |-- middlewares.py		中间件配置  
            |-- pipelines.py		管道  
            |-- settings.py			爬虫配置  
            |-- __init__.py   
            |-- spiders				爬虫实例目录  
            |   |-- rankingspider.py 排行榜爬虫实例  
            |   |-- test01.py  
            |   |-- userspider.py 		用户和自定义爬虫实例 
            |   |-- __init__.py   
            |   |-- unittest		单元测试相关文件   
## 文件`rankingspider.py`架构。
+ 简单说明，之后再详细说明。
1. 请求交给`ProxyHandlerMiddleware`自动获取代理，这个中间件可以关闭【注意开启后必须有代理，否则不会成功】
2. 之后交给`SeleniumInterceptMiddleware`，由selenium打开目标url，爬取排行榜信息。
3. 此时浏览器挂机，`scrapy`爬取api接口获得视频`aid` `cid` `bid`和`metadata`。
4. 将`VideoInfoItem`交给`RankingPipeline`，解析视频地址列表。
5. 从视频列表向`线程池`提交下载任务。
7. 如果代理IP下载失败则放入`失败队列`，同时删除这个代理IP。
8. 失败队列`重新选择代理`下载这个视频。
6. 爬虫结束后关闭selenium保存错误日志、关闭任务队列。 

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

# 其他 
## 附录
+ 附录表结构：
```Mysql
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