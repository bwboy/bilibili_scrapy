# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import hashlib,time
from scrapy.http import HtmlResponse
from twisted.internet import defer, threads
import threading
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
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
        if spider.name == "test01":
            if not 'web-interface' in request.url and not  '.mp4' in request.url:
                spider.browser.get(request.url)
                spider.browser.add_cookie({'SESSDATA':'aa15d6af%2C1560734457%2Ccc8ca251'})
                time.sleep(2)
                if "ranking" in request.url:
                    spider.browser.find_element_by_xpath('//ul[@class="rank-tab"]/li[{}]'.format(spider.TARGET_CLASS)).click()
                time.sleep(4)
                print('访问：{}'.format(request.url))
                #这里直接retrun HtmlResponse的原因是我们已经通过模拟浏览器的方式访问过一遍网站了 不需要再次进入downloader下载一次所以直接return就好了
                time.sleep(2)
                return HtmlResponse(url=spider.browser.current_url,body=spider.browser.page_source,encoding='utf-8')
            else:
                print("获取到了一个视频下载地址："+request.url)

        if spider.name == "rankingspider":
            if "ranking" in request.url:
                spider.browser.get(request.url)
                if "ranking" in request.url:
                    spider.browser.implicitly_wait(10)
                    spider.browser.find_element_by_xpath('//ul[@class="rank-tab"]/li[{}]'.format(spider.TARGET_CLASS)).click()
                time.sleep(2)
                print('访问：{}'.format(request.url))
                return HtmlResponse(url=spider.browser.current_url,body=spider.browser.page_source,encoding='utf-8')




class ProxyHandlerMiddleware(object):
    headers = {
            'Host': 'bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
    access_list=[]
    executor = ThreadPoolExecutor(max_workers=5)
    thread_list=[]

    def process_request(self, request, spider):
        if spider.name == "rankingspider":
            if "ranking" in request.url:
                spider.EnableProxy=True
                self.access_list=spider.PROXIES_LIST
                self.getProxyList(spider)
                if len(self.access_list)==0:
                    raise RuntimeError('【警告】没有获取到代理地址，爬虫不会进行！[Warning] If the proxy address is not obtained, the crawler will not proceed!')
                print("一共获取到代理个数：{}".format(len(self.access_list)))
        return None


    ''' 获取代理 '''
    def getProxyList(self,spider):
        spider.browser.get("https://www.xicidaili.com/nn/")
        js="document.documentElement.scrollTop="+ str(500)
        spider.browser.execute_script(js)
        tr = spider.browser.find_elements_by_xpath('//tr[@class="odd"]')
        time.sleep(4)


        current_list=[]
        i=1
        for td in tr:
            try:
                ip=spider.browser.find_element_by_xpath('//tr[{}]/td[2]'.format(i+1)).text
                port=spider.browser.find_element_by_xpath('//tr[{}]/td[3]'.format(i+1)).text
            except NoSuchElementException:
                print('ip、端口元素未找到')
            current_list.append('{}:{}'.format(ip,port))
            print('{}:{}'.format(ip,port))
            i+=1
            if i==len(tr):
                break
        
        for li in current_list:
            task = self.executor.submit(self.test_proxy,spider.URL,li,self.headers)
            self.thread_list.append(task)
        wait(self.thread_list, return_when=ALL_COMPLETED)
        self.executor.shutdown()
        print('{}个代理可以使用,一共检测到{}个代理。'.format(len(self.access_list),len(current_list)))
        return self.access_list

    ''' 测试代理 '''
    def test_proxy(self,test_url,li,headers):
        
        proxy_temp={"http":li}
        try:
            res = requests.get(test_url,headers=headers,proxies=proxy_temp,verify=False,timeout=5)
            self.access_list.append(proxy_temp)
        except Exception as e:
            print(li+"  is delete"+'-------')
    def process_response(self, request, response, spider):
        return response

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
