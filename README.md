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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=224 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```