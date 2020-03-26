# -*- coding: utf-8 -*-

# Scrapy settings for bilibili project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'bilibili'

SPIDER_MODULES = ['bilibili.spiders']
NEWSPIDER_MODULE = 'bilibili.spiders'

#下载地址
DOWNLOAD_DIR=r"F:\study_project\webpack\scrapy"
#chrome驱动地址
WEBDRIVER_PATH=r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe'
#mysql配置
MYSQL_CONFIG={"host":'127.0.0.1',
            "port":3306,
            "user":'wxwmodder',
            "password":'sxmc321',
            "db":'scrapy01'}
#Mongo配置
MONGO_CONFIG='mongodb://root:root@127.0.0.1:27017/admin'
def getMongoConfig():
    return MONGO_CONFIG
def getMySQLConfig():
    return MYSQL_CONFIG
def getDownloadDir():
   return DOWNLOAD_DIR
def getWebDriverPath():
   return WEBDRIVER_PATH
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bilibili (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Cookie': 'SESSDATA=aa15d6af%2C1560734457%2Ccc8ca251', # 登录B站后复制一下cookie中的SESSDATA字段,有效期1个月
        'Host': 'api.bilibili.com'
    }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   #'bilibili.middlewares.BilibiliSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'bilibili.middlewares.BilibiliDownloaderMiddleware': 543,
   # 'bilibili.middlewares.ProxyHandlerMiddleware': 1,
   'bilibili.middlewares.SeleniumInterceptMiddleware': 2,
}
# LOG_LEVEL ='WARNING'
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #'bilibili.pipelines.BilibiliPipeline': 300,
   # 'bilibili.pipelines.DownloadVideoPipeline':301,
   'bilibili.pipelines.RankingPipeline':302,
   # 'bilibili.pipelines.MysqlPipeline':350,
   # 'bilibili.pipelines.MongoPipeline':352,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
