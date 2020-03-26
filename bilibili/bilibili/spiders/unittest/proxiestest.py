from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from selenium.webdriver.chrome.options import Options

import requests
from requests.exceptions import *
import time
from threading import Thread
import random


access_list=[]
def proxy_get(base_url,test_url,page=1):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe',chrome_options = chrome_options)
    browser.get(base_url)
    
    headers = {
        'Host': 'wx2.sinaimg.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    browser.implicitly_wait(10)
    js="document.documentElement.scrollTop="+ str(500)
    browser.execute_script(js)
    time.sleep(5)

    current_page=0
    current_list=[]

    while current_page != page:
        '''爬取'''
        tr = browser.find_elements_by_xpath('//tr[@class="odd"]')
        i=1
        for td in tr:
            '''

            https://ip.ihuan.me/
            ip=browser.find_element_by_xpath('//tr[{}]/td[@data-title="IP"]'.format(i)).text
            port=browser.find_element_by_xpath('//tr[{}]/td[@data-title="PORT"]'.format(i)).text
            next_page=browser.find_element_by_xpath('//a[@aria-label="Next"]')

            https://www.xicidaili.com/nn/   
            tr = browser.find_elements_by_xpath('//tr[@class="odd"]')
            ip=browser.find_element_by_xpath('//tr[{}]/td[2]'.format(i)).text
            port=browser.find_element_by_xpath('//tr[{}]/td[3]'.format(i)).text

            https://lab.crossincode.com/proxy/
            tr = browser.find_elements_by_xpath('//tr[2]')
            ip=browser.find_element_by_xpath('//tr[{}]/td[1]'.format(i)).text
            port=browser.find_element_by_xpath('//tr[{}]/td[2]'.format(i)).text
            '''
            try:
                ip=browser.find_element_by_xpath('//tr[{}]/td[2]'.format(i+1)).text
                print("------------------------"+ip)
                port=browser.find_element_by_xpath('//tr[{}]/td[3]'.format(i+1)).text
            except NoSuchElementException:
                print('ip、端口元素未找到')
            current_list.append('{}:{}'.format(ip,port))
            print('{}:{}'.format(ip,port))
            i+=1
            if i==len(tr):
                break

        try:
            next_page=browser.find_element_by_xpath('//a[@aria-label="Next"]')    # 查找指定元素
            next_page.click()
        except NoSuchElementException:             # 捕获是否找不到元素
            print("没有找到下一页按钮位置。")
            break
        # finally:
            # browser.close()
        current_page+=1

    executor = ThreadPoolExecutor(max_workers=5)
    thread_list=[]
    for li in current_list:
        task = executor.submit(test_proxy,test_url,li,headers)
        thread_list.append(task)
    wait(thread_list, return_when=ALL_COMPLETED)
    executor.shutdown()
    print('{}个代理可以使用,一共检测到{}个代理。'.format(len(access_list),len(current_list)))
    return access_list





def test_proxy(test_url,li,headers):
    global access_list
    proxy_temp={"http":li}
    try:
        res = requests.get(test_url,headers=headers,proxies=proxy_temp,verify=False,timeout=5).status_code
        access_list.append(proxy_temp)
    except Exception as e:
        print(li+"  is delete"+'-------')
        print(e)
        

if __name__ == "__main__":
    # https://ip.ihuan.me/
    ip_list=proxy_get('https://www.xicidaili.com/nn/','https://www.kuaidaili.com/free/inha/1/')  #https://www.kuaidaili.com/free/inha/
    for i in ip_list:
        print(i)
    print(random.choice(ip_list))
