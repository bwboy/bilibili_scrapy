import requests
import ssl
import re,os,json
import urllib.parse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
#初始化全局配置。
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"')


download_dir=r'F:/study_project/webpack/scrapy'

import urllib.request
from urllib import request, parse

def urllib_request(url):
    # request = urllib.request.Requests('https://python.org')
    # response = urllib.request.urlopen(request)
    # print(response.read().decode('utf-8'))

    # 增加header

    # url = 'http://httpbin.org/post'
    headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "connection": "Keep-Alive",
        "accept": "*/*",
            }
    # # 构造POST表格
    # dict = {
    #     'name':'Germey'
    # }
    # data = bytes(parse.urlencode(dict),encoding='utf8')
    req = request.Request(url=url,headers=headers,method='GET')
    response = request.urlopen(req)
    return response.read().decode('utf-8')



def getBaidu():
    url="http://v.baidu.com/watch/670898235286398193.html"
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }
    res=requests.get(url,headers=headers)
    html=res.text


    start=html.find("videoFlashPlayUrl")+len("videoFlashPlayUrl = '")
    print(start)

    end=html.find("videoFlashPlayUrl",start)

    target_end=html.rfind("';",start,end)

    swf_url=html[start:target_end]

    start=swf_url.find("video=")+len("video=")

    stream_url=urllib.parse.unquote(swf_url[start:])   

    download_mp4(stream_url,download_dir,"baidu_video")

    print(stream_url)

def download_mp4(video_url,download_dir,video_title):
    response_stream=requests.get(url=video_url,stream=True)
    if not os.path.exists(download_dir+'/{}'.format(video_title)):
        os.makedirs(download_dir+'/{}'.format(video_title))
    f = open("{0}/{1}/{2}.mp4".format(download_dir,video_title,video_title),'wb+')
    for chunk in response_stream.iter_content(chunk_size=1024):# 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
        if chunk:
            f.write(chunk)
    f.close()
    print("视频下载完成:{}".format("{0}/{1}/{2}.mp4".format(download_dir,video_title,video_title)))

def download_mp4list(video_url,download_dir,video_title,COUNT):
    print(video_url)

    
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "connection": "Keep-Alive",
        "accept": "*/*",
        }

    cookies_str='P_F=1; firstExpireTime=1586846343614; P_T=1586778449; firstTimes=0; __ysuid=1578988773054FaX; UM_distinctid=17162b8e508106-0f734989114434-396a4605-144000-17162b8e5092b4; cna=CDT5FYlWrxcCAQFfOLjhX9s0; __aysid=1586755781014HcC; __ayscnt=1; __ayft=1586759462411; P_ck_ctl=E52E8F4FBF78161A5CA5AC9CDA683E59; modalFrequency={"UUID":"1"}; modalBlackListclose={"UUID":"1"}; modalBlackListlogined={"UUID":"1"}; isg=BFtb3CbigXcmBf0GM1q9CiWQ6r_FMG8y-EpSak2YeNpxLHoO1QDXg_ZlxoyiDMcq; __arpvid=1586947454908ZJVqZP-1586947454980; __arycid=dd-3-00; __arcms=dd-3-00; __aypstp=31; __ayspstp=31; _m_h5_tk=5d274e2f14ddf5a7b56fc36f5772c10e_1586951055900; _m_h5_tk_enc=d77d83ba7c4531e76b126aaf52104cd0; _m_h5_c=72ebb9b892fb007301716c170e20a392_1586955016961%3Bfaac475c3fa5b5e47e659c8ecdab1920; __ayvstp=17; __aysvstp=17'
    cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookies_str.split("; ")}


    urllib.request.urlretrieve(video_url,"{0}/{1}/{2:03d}.ts".format(download_dir,video_title,COUNT))

    # response_stream=requests.get(video_url,headers=send_headers,cookies=cookie_dict,verify=False)
    # if not os.path.exists(download_dir+'/{}'.format(video_title)):
    #     os.makedirs(download_dir+'/{}'.format(video_title))
    # f = open("{0}/{1}/{2:03d}.ts".format(download_dir,video_title,COUNT),'wb+')
    # for chunk in response_stream.iter_content(chunk_size=1024):# 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
    #     if chunk:
    #         f.write(chunk)
    # f.close()
    print("视频下载完成:{}".format("{0}/{1}/{2}.ts".format(download_dir,video_title,COUNT)))

if __name__ == "__main__":
    # getBaidu()

    url_list=['http://vali-dns.cp31.ott.cibntv.net/6572C0C07B44671D01E6D4D4F/03002007005E7AFA1F8BB7800000000ECBEBF8-F162-4077-AE34-E8728787B6DE.mp4?ccode=0502&duration=390&expire=18000&psid=00437ba43df4739fcb7b35abc0705573&ups_client_netip=015f4277&ups_ts=1586947469&ups_userid=&utid=CDT5FYlWrxcCAQFfOLjhX9s0&vid=XNDU5NjIwMjAwOA&vkey=Bb99bbb1e2165d20cc335cbc005c33913&eo=1&bc=2&dre=u17&si=45&dst=1',
    'http://vali-dns.cp31.ott.cibntv.net/657370F0C1A4171AE7CAF25E8/03002007015E7AFA1F8BB7800000000ECBEBF8-F162-4077-AE34-E8728787B6DE.mp4?ccode=0502&duration=390&expire=18000&psid=00437ba43df4739fcb7b35abc0705573&ups_client_netip=015f4277&ups_ts=1586947469&ups_userid=&utid=CDT5FYlWrxcCAQFfOLjhX9s0&vid=XNDU5NjIwMjAwOA&vkey=B5b9554c7d716e651e8114e1abd5242ad&eo=1&bc=2&dre=u17&si=45&dst=1',
     "http://vali-dns.cp31.ott.cibntv.net/677581807184A71EB063848A4/03002007025E7AFA1F8BB7800000000ECBEBF8-F162-4077-AE34-E8728787B6DE.mp4?ccode=0502&duration=390&expire=18000&psid=00437ba43df4739fcb7b35abc0705573&ups_client_netip=015f4277&ups_ts=1586947469&ups_userid=&utid=CDT5FYlWrxcCAQFfOLjhX9s0&vid=XNDU5NjIwMjAwOA&vkey=B259cc5794721fbe625e42a9e48939ff3&eo=1&bc=2&dre=u17&si=45&dst=1",
     "http://vali-dns.cp31.ott.cibntv.net/677631B0A164D71FF341069E5/03002007035E7AFA1F8BB7800000000ECBEBF8-F162-4077-AE34-E8728787B6DE.mp4?ccode=0502&duration=390&expire=18000&psid=00437ba43df4739fcb7b35abc0705573&ups_client_netip=015f4277&ups_ts=1586947469&ups_userid=&utid=CDT5FYlWrxcCAQFfOLjhX9s0&vid=XNDU5NjIwMjAwOA&vkey=Bf5ea14db8fb9aed99175c8546b14a562&eo=1&bc=2&dre=u17&si=45&dst=1",
     "http://vali-dns.cp31.ott.cibntv.net/6776E1E060B4A71EB06384E7B/03002007045E7AFA1F8BB7800000000ECBEBF8-F162-4077-AE34-E8728787B6DE.mp4?ccode=0502&duration=390&expire=18000&psid=00437ba43df4739fcb7b35abc0705573&ups_client_netip=015f4277&ups_ts=1586947469&ups_userid=&utid=CDT5FYlWrxcCAQFfOLjhX9s0&vid=XNDU5NjIwMjAwOA&vkey=Bfaf382796a58590a39f4f8ae00779f3b&eo=1&bc=2&dre=u17&si=45&dst=1",
     "http://vali-dns.cp31.ott.cibntv.net/6978F270C3F4171AE7CAF603A/03002007055E7AFA1F8BB7800000000ECBEBF8-F162-4077-AE34-E8728787B6DE.mp4?ccode=0502&duration=390&expire=18000&psid=00437ba43df4739fcb7b35abc0705573&ups_client_netip=015f4277&ups_ts=1586947469&ups_userid=&utid=CDT5FYlWrxcCAQFfOLjhX9s0&vid=XNDU5NjIwMjAwOA&vkey=Bfbb374170fd142a09ccc9e77872691c3&eo=1&bc=2&dre=u17&si=45&dst=1",
     "http://vali-dns.cp31.ott.cibntv.net/677842408A13471570B5B36B2/03002007065E7AFA1F8BB7800000000ECBEBF8-F162-4077-AE34-E8728787B6DE.mp4?ccode=0502&duration=321&expire=18000&psid=00437ba43df4739fcb7b35abc0705573&ups_client_netip=015f4277&ups_ts=1586947469&ups_userid=&utid=CDT5FYlWrxcCAQFfOLjhX9s0&vid=XNDU5NjIwMjAwOA&vkey=B28a9f4d4355d281432a88cea1f3fe578&eo=1&bc=2&dre=u17&si=45&dst=1"
]

    # COUNT=1
    # for url in url_list:
    #     download_mp4list(url,download_dir,"xxxxxx",COUNT)
    #     COUNT+=1

    url='https://valipl.cp31.ott.cibntv.net/6774744E42B4E7205F41B2633/03000500005E7AFA2A8BB78000000072802AC8-8FE2-452C-BBFD-2313989F2E41.m3u8?ccode=0502&duration=2661&expire=18000&psid=773f98eb6f7a1391660a4254c1711a32&ups_client_netip=015f4277&ups_ts=1587020444&ups_userid=&utid=CDT5FYlWrxcCAQFfOLjhX9s0&vid=XNDU5NjIwMjAwOA&vkey=B2b985d73ff014f9b09c19af86a7e0653&sm=1&operate_type=1&dre=u37&si=73&eo=1&dst=1&iv=0&s=efbfbd75267cefbfbd26&type=flvhdv3&bc=2'
    # res=urllib_request(url)
    # m3u8_list=res.split(",")[1:]

    # 110.83.46.180:808

    res=requests.get(url)
    m3u8_list=res.text.split(",")[1:]

    ts_list=[]
    for i in m3u8_list:
        start=i.find("http")
        end=i.find("#",start)
        url=i[start:end]
        ts_list.append(url)

    COUNT=1
    for item in ts_list:
        download_mp4list(item,download_dir,"xxxxxx",COUNT)
        COUNT+=1

        # if COUNT==5:
        #     break


