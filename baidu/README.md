@[TOC](python百度视频爬虫与scrapy拓展)
# 快速开始
1. 克隆或拉取项目后，请安装依赖模块： 
`pip install -r requirements.txt`

2. 设置下载目录，打开"`baidu/baidu/setting.py`"
	```python
	# 下载目录
	DOWNLOAD_DIR=r"F:\study_project\webpack\scrapy"
	# chrome驱动路径因为土豆网特殊加密，视频流必须由selenium+chrome渲染界面后获取
	```
3. 切换到目录"`./baidu/`"
	```cmd
	scrapy crawl multiple
	```
	回车后根据提示输入或者不输入参数
4. 此时就可以看到你所设置的目录中下载好的文件了。 
# 配置说明
## 爬虫`multiple`，自定义爬取  
+ **多个视频:** 刚才的例子中，我们使用了multiple爬取了两个视频。若要自己添加多个视频。可以打开"`\baidu\baidu\spiders\multiple.py`"
	```python
	   # 单个视频的连接，有多少个写多少个
	    start_urls = ['http://v.baidu.com/watch/670898235286398193.html',
	    'http://v.baidu.com/watch/6732132984955826029.html']
	```
## 爬虫`ranking`，排行榜爬取。 
基本上参数配置和上面差不多。但是这里支持参数热传入。直接执行就会提示你需要输入的参数。
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
	#    'baidu.pipelines.BaiduPipeline': 300,
	   'baidu.pipelines.RankingPipeline': 50,
	#    'baidu.pipelines.MysqlPipeline': 51,
	#    'baidu.pipelines.MongoPipeline': 51,
	}
	```
# 代理  
目录中有个`proxy.txt`，把代理添加进去。
+ 自定义代理列表。爬虫中都包含了，可自定义配置代理列表。**注意**，*当代理列表不为空时，下载将随机使用代理，如果出错将在代理列表中重新选择，如果重试5次仍然失败则跳过。*如果为空。将不使用代理。
	```python
	PROXIES_LIST=[] 
	#[{"http":"117.94.213.117:8118"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"},{"http":"127.0.0.1:8080"}]
	```

# 百度视频Url分析  
百度视频页面url形如`http://v.baidu.com/watch/6292038733512290509.html`，请求这个页面就会得到一个flash播放地址。得到的url页面中会有一行以：
` var videoFlashPlayUrl = 'http://list.video.baidu.com/swf/ecomAdvPlayer.swf?tpl=coop&controls=progress,pause,volumn,fullscreen&video=http%3A%2F%2Fpgcvideo.cdn.xiaodutv.com%2F1464979428_939503821_2020041915000320200419171914.mp4%3FCache-Control%3Dmax-age%253D8640000%26responseExpires%3DTue%252C%2B28%2BJul%2B2020%2B17%253A46%253A55%2BGMT%26xcode%3Db53d76887290f4e9a2798c14d141e0d0c072609261fd023a%26time%3D1587463750';
`
1. 得到视频流地址。  
你会发现里面有个参数是`&video=`，后面跟着参数。`http%3A%2F%2Fpgcvideo.cdn.xiaodutv.com%2F1464979428_939503821_2020041915000320200419171914.mp4%3FCache-Control%3Dmax-age%253D8640000%26responseExpires%3DTue%252C%2B28%2BJul%2B2020%2B17%253A46%253A55%2BGMT%26xcode%3Db53d76887290f4e9a2798c14d141e0d0c072609261fd023a%26time%3D1587463750`
2. 解码url  
上面的url通过转码得到`http://pgcvideo.cdn.xiaodutv.com/1464979428_939503821_2020041915000320200419171914.mp4?Cache-Control=max-age%3D8640000&responseExpires=Tue%2C+28+Jul+2020+17%3A46%3A55+GMT&xcode=b53d76887290f4e9a2798c14d141e0d0c072609261fd023a&time=1587463750`
这个地址就是视频播放地址。
3. 访问这个地址就得到流视频文件。

# 附录
+ 数据库结构
	```sql
	CREATE TABLE `baidu_info` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	  `author` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	  `hot` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	  `img_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	  `pub_time` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	  `href` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	  `stream_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	  `file_content` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	```