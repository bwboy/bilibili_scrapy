



@[TOC](python土豆网视频爬虫与scrapy拓展)
# 快速开始
1. 克隆或拉取项目后，请安装依赖模块： 
`pip install -r requirements.txt`

2. 设置下载目录，打开"`tudou/tudou/setting.py`"
	```python
	# 下载目录
	DOWNLOAD_DIR=r"F:\study_project\webpack\scrapy"
	# chrome驱动路径因为土豆网特殊加密，视频流必须由selenium+chrome渲染界面后获取
	# Linux注意下载chrome和对应的linux版本driver
	WEBDRIVER_PATH=r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe'
	```
3. 切换到目录"`./tudou/`"
	```cmd
	scrapy crawl multiple
	```
	回车后根据提示输入或者不输入参数
4. 此时就可以看到你所设置的目录中下载好的文件了。 

# 配置说明
## 爬虫`multiple`，自定义爬取  
+ **多个视频:** 刚才的例子中，我们使用了multiple爬取了两个视频。若要自己添加多个视频。可以打开"`\tudou\tudou\spiders\multiple.py`"
	```python
    # 单个视频的连接，有多少个写多少个
    start_urls = ['https://video.tudou.com/v/XNDQ0OTU2NDMxNg',
    'https://video.tudou.com/v/XNDUyMjc3NzgyMA==.html?spm=a2h28.8313461.feed.dvideo']
	```
## 爬虫`ranking`，排行榜爬取。 
基本上参数配置和上面差不多。但是这里支持参数热传入。直接执行就会提示你需要输入的参数。`确保你设置了chrome驱动路径。`
```cmd
scrapy crawl ranking
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
	#    'tudou.pipelines.TudouPipeline': 300,
	   'tudou.pipelines.RankingPipeline': 50,
	#    'tudou.pipelines.MysqlPipeline': 51,
	#    'tudou.pipelines.MongoPipeline': 51,
	}
	```
# 代理  
目录中有个`proxy.txt`，把代理添加进去。
+ 自定义代理列表。爬虫中都包含了，可自定义配置代理列表。**注意**，*当代理列表不为空时，下载将随机使用代理，如果出错将在代理列表中重新选择，如果重试5次仍然失败则跳过。*如果为空。将不使用代理。
	```python
	PROXIES_LIST=[] 
	#[{"http":"117.94.213.117:8118"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"}]
	```
# 土豆网视频Url分析  
土豆网视频流包含在`https://ups.youku.com/ups/get.json`接口中，但访问这个接口所需要携带的参数过多，但我发现可以在页面上直接找到`包含参数的视频api`。
## 获取json  
+ 以`https://video.tudou.com/v/XNDQ0OTU2NDMxNg==.html?spm=a2h28.8313461.feed.dvideo`为例。我们用selenium访问渲染后的响应体。

+ 等待selenium渲染之后会在页面插入如下标签
	```html
	<script src="https://ups.youku.com/ups/get.json?
	vid=1112391079&amp;
	ccode=050F&amp;
	client_ip=192.168.1.1&amp;
	utid=CDT5FYlWrxcCAQFfOLjhX9s0&amp;
	client_ts=1586758924&amp;
	ckey=122%2343bzHJoyEE%2Bt6DpZy4pjEJponDJE7SNEEP7ZpJRBuDPpJFQLpCGw2HZDpJEL7SwBEyGZpJLlu4Ep%2BFQLpoGUEELWn4yE7SNEEP7ZpERBuDPE%2BBQPpC76EJponDJLKMQEIm0xXDnTtByWAfaPwr8S14Rqur0Qq1I2zXs%2Bo3T93j%2BpQrdanZzhqz7oYWlkNgp1uO0%2FDLVr8p76%2B4EEyFfDqM3bDEpxngR4ul5EDtgPm4AiJDbEfC3mqM3WE8pangL4ul0EDLVr8CpU%2B4EEyFfDqMfbDEpxnSp4uOIEELXZ8oL6JwTEyF3F7S32DEp6dSxwuAuROrJsNoRiAJPvhEt6unFLzrzz9dAYrKzg0B%2FkEqkZc64LUiTq5Div0t55hL7QYgfDFaS6Wtwwt%2FGWw0JgUMZ4brsMAb55mEtDfxAm4c23XhfHdIj%2FreonACxavy2C6IMxHKwdSzik4Ygb5LpVFTMFl373SdSFbUdlHDhZW6iebml5K2kG2Qt7VVWAyKBCc%2BsLtbH8B6ndziphr45ToQC3L6Fqa6jEfdWsYE7FEjRKAw%2FJAwjmle4PUwxokuecbLoeV7yw0o%2BXBoPU7FNkHEpNJbP5GNXw8QMkyDCmBcizolVRXtafzbhxiMnhEUtp&amp;
	site=-1&amp;
	wintype=interior&amp;
	p=1&amp;
	fu=0&amp;
	vs=1.0&amp;
	rst=mp4&amp;
	dq=flv&amp;
	os=win&amp;osv=&amp;d=0&amp;
	bt=pc&amp;aw=w&amp;needbf=1&amp;
	callback=youkuPlayer_call_1586758924663&amp;_t=043752610994792995"></script>
	```
+ 解码、请求标签里的src就会获得一个json数组。`stream.segs[0].cdn_url`就包含了视频流文件。
	```python
	stream=data['stream']
	mp4_list=[]
	for item in stream:
	    download_url=item['segs'][0]['cdn_url']
	    mp4_list.append(download_url)
	    print(download_url)
	print(mp4_list[-1])
	```

# 附录  
+ 数据库结构
	```sql
	CREATE TABLE `tudou_info` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	`reply` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	`author` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	`pub_time` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	`file_content` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	`img_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	`href` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	`stream_url` text COLLATE utf8mb4_unicode_ci,
	PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	```

+ 土豆解决方案-  需要下载m3u8，可直接下载视频。

+ 搜狐 - mp4 搜索可直接下载

+ PPTV - m3u8 文件包含在返回值中，可直接下载。

+ 百度 - MP4 请求到了主页面，可从js中查找就可以直接下载。

+ 凤凰视频 - m3u8 混合 mp4 但视频可直接下载。

+ 芒果 - m3u8 但是需要携带请求头，不能直接下载ts

+ 腾讯视频 js提取：参考文档 https://blog.csdn.net/qq_43546676/article/details/88980704

