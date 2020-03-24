# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import hashlib
import time
from scrapy.http import HtmlResponse
from twisted.internet import defer, threads
# from tender_scrapy.extendsion.selenium.spider import SeleniumSpider
# from tender_scrapy.extendsion.selenium.requests import SeleniumRequest

""" 
@author:吴晓伟
@description:
    负责返回浏览器渲染后的Response
"""
class SeleniumInterceptMiddleware(object):
    #通过chrome请求动态网页
    def process_request(self, request, spider):
    	#这里的XXXX即为我们的爬虫名,对不同的爬虫进行动态的修改
        print("---------url:{}-------------------".format(request.url))
        if spider.name == "test01":
            if not 'web-interface' in request.url and not  '.mp4' in request.url:
                spider.browser.get(request.url)
                spider.browser.add_cookie({'SESSDATA':'aa15d6af%2C1560734457%2Ccc8ca251'})
                import time
                if "ranking" in request.url:
                    spider.browser.find_element_by_xpath('//ul[@class="rank-tab"]/li[{}]'.format(spider.TARGET_CLASS)).click()
                time.sleep(4)
                print('访问：{}'.format(request.url))
                #这里直接retrun HtmlResponse的原因是我们已经通过模拟浏览器的方式访问过一遍网站了 不需要再次进入downloader下载一次所以直接return就好了
                return HtmlResponse(url=spider.browser.current_url,body=spider.browser.page_source,encoding='utf-8')
            else:
                print("获取到了一个视频下载地址："+request.url)

        if spider.name == "rankingspider":
            if "ranking" in request.url:
                spider.browser.get(request.url)
                import time
                if "ranking" in request.url:
                    spider.browser.find_element_by_xpath('//ul[@class="rank-tab"]/li[{}]'.format(spider.TARGET_CLASS)).click()
                time.sleep(4)
                print('访问：{}'.format(request.url))
                #这里直接retrun HtmlResponse的原因是我们已经通过模拟浏览器的方式访问过一遍网站了 不需要再次进入downloader下载一次所以直接return就好了
                return HtmlResponse(url=spider.browser.current_url,body=spider.browser.page_source,encoding='utf-8')





""" 
@author:吴晓伟
@description:
    负责下载视频的中间件。
"""
class DownloadVideoMiddleware(object):
    def process_request(self, request, spider):
    	#这里的XXXX即为我们的爬虫名,对不同的爬虫进行动态的修改
        if spider.name == "test01":
            if 'web-interface' in request.url:
                pass

class BilibiliSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
