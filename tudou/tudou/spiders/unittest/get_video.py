import requests
import ssl
import re,os,json


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

def get_first_url():
    addr="https://video.tudou.com/v/XNDQxOTgwODEyMA==.html?spm=a2h28.8313461.feed.dvideo"
    browser = webdriver.Chrome(r'F:\study_project\webpack\SeleniumDemo\chromedriver.exe',chrome_options=chrome_options)
    browser.set_page_load_timeout(4)
    

    try:
        browser.get(addr)
    except TimeoutException as e:
        print("加载页面太慢，停止加载，继续下一步操作")
        browser.execute_script('window.stop()')

    url_list=[]

    for i in range(1,20):
        url_list.append(browser.find_element_by_xpath("/html/head/script[{}]".format(i)).get_attribute('src'))


    callback_url=""
    for url in url_list:
        if "ups.youku.com/ups/get.json" in url:
            callback_url=url
            break
    print("callback地址：{}".format(callback_url))
    # get_mp4_from_js(addr,callback_url)

'''
author:吴晓伟
desc：用于测试下载流视频可行性的代码片段。完全使用面向过程编程，便于理解。
'''

download_dir=r'F:/study_project/webpack/scrapy'

''' 测试requests 分段下载视频数据 每个数据块1024 '''
def download_video_chip(video_url,headers,download_dir,video_title,chip):
    response_stream=requests.get(url=video_url,headers=headers,stream=True)
    if not os.path.exists(download_dir+'/{}'.format(video_title)):
        os.makedirs(download_dir+'/{}'.format(video_title))
    f = open("{0}/{1}/{2:04d}.ts".format(download_dir,video_title,chip),'wb+')
    for chunk in response_stream.iter_content(chunk_size=1024):# 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
        if chunk:
            f.write(chunk)
    f.close()
    print("视频下载完成:{}".format(chip))

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


def souhuo_download():  #video_url,headers,video_title
    headers={
        # 'Origin': 'https://tv.sohu.com',
        # 'Referer': 'https://tv.sohu.com/v/MjAxNTAxMDUvbjQwNzU0MzI0My5zaHRtbA==.html?fid=784&pvid=4d4db6d26aa0a4ec',
        # 'Sec-Fetch-Mode': 'no-cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }
    video_url="http://list.video.baidu.com/swf/ecomAdvPlayer.swf?tpl=coop&controls=progress,pause,volumn,fullscreen&video=http%3A%2F%2Fpgcvideo.cdn.xiaodutv.com%2F2938077641_1730706785_20190505183107.mp4%3FCache-Control%253Dmax-age%253A8640000%2526responseExpires%253DTue%252C_13_Aug_2019_18%253A31%253A46_GMT%3D%26xcode%3Debc73a2071fc3947f0436b82ce595ec8b7ae3f890d334781%26time%3D1586946112"
    video_title="souhu_video"


    response_stream=requests.get(url=video_url,stream=True,headers=headers)
    if not os.path.exists(download_dir+'/{}'.format(video_title)):
        os.makedirs(download_dir+'/{}'.format(video_title))
    f = open("{0}/{1}/{2}.mp4".format(download_dir,video_title,video_title),'wb+')
    for chunk in response_stream.iter_content(chunk_size=1024):# 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
        if chunk:
            f.write(chunk)
    f.close()
    print("视频下载完成:{}".format("{0}/{1}/{2}.mp4".format(download_dir,video_title,video_title)))

def start_url():
    m3u8 = 'http://pl-ali.youku.com/playlist/m3u8?vid=1136718237&type=hd2&ups_client_netip=015f221b&utid=CDT5FYlWrxcCAQFfOLjhX9s0&ccode=050F&psid=67448f6badcc1b83352616f7e12d4403&duration=233&expire=18000&drm_type=1&drm_device=7&dyt=1&ups_ts=1586236809&onOff=0&encr=0&ups_key=6d7fd981ab4189a466bf6f13f82c41d5'

    res=requests.get(m3u8)
    data= bytes.decode(res.content)

    chips=data.split(",")[1:]
    count=0
    for item in chips:
        download_url=item.split("#")[0]
        # print(download_url)
        download_video(download_url,download_dir,'tudou_video',count)
        count+=1
def get_mp4_from_js(referer,callback):
    headers={
        "Referer": referer,
        "Sec-Fetch-Mode": "no-cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }

    js_file_url=callback  #'https://ups.youku.com/ups/get.json?vid=1104952030&amp&ccode=050F&amp&client_ip=192.168.1.1&amp&utid=tEYUF%2FSgvg8CAQFfIhtZ74Zk&amp&client_ts=1586321620&amp&ckey=122%23Bk2Y345eEEa%2BxEpZy4pjEJponDJE7SNEEP7ZpJRBuDPpJFQLpCGw2HZDpJEL7SwBEyGZpJLlu4Ep%2BFQLpoGUEELWn4yE7SNEEP7ZpERBuDPE%2BBQPpC76EJponDJLKMQEIm0xXDnTtByWAfaPwr8S14Rqur0Qq1I2zXs%2Bo3T93j%2BpQrdanZzhqz7oYWlOJSp1uOjtDLVr82f6%2B4EEyFfDqM3bDEpxngR4ul5EDtgPm4AiJDbEfC3mqM3WE8pangL4ul0EDLVr8CpU%2B4EEyFfDqMfbDEpxnSp4uOIEELXZ8oL6JwTEyF3F7S32DEp6dSxwuAuROrJsNoRiUEVs44MIGRkP%2Be7FHr5z9vGoSwxD3ge9AueBUrvgxR19L2RPflw0jTgIV5fnm8s3L5PsT4tS%2FcRypKDbVRSfLKBc5UzNZ8ZcYS9WVeUJFLaTGKaaPUhzwH0Q9WAoFJo1xwSeq4F95rUSEcgHIf8tWu0xbSjQvO4SRGzEpVs5l0w6g2wzDXX8xeh5dKXqPWvI9NRKeLV2fTae5Jwl5ePiV548p3eZVU6X1prsOqdSKucGeDO%2BI0kozH79J7THb0SAU0BMzz%2BJ7xrdLe1FrWL%2FdPjymQbIWpUHPHfC7tjLLKmzH0mWh5fOT%2FqiJy0ee4ksyVpLK2I%2BF9jl5qeaftIWFSWHCNnnnnqApSHwKoEHZP4e7k1jnFSO4QKnCLMPgT2xmg9AvxDvW4lcQfg7v0l%3D&amp&site=-1&amp&wintype=interior&amp&p=1&amp&fu=0&amp&vs=1.0&amp&rst=mp4&amp&dq=flv&amp&os=win&amp&osv=&amp&d=0&amp&bt=pc&amp&aw=w&amp&needbf=1&amp&callback=youkuPlayer_call_1586321620291&amp&_t=09926404957293145'

    res=requests.get(url=js_file_url,headers=headers)
    data_text=res.text#  bytes.decode(res.content)
    start= data_text.find("(")+1
    end=data_text.rfind(")")
    data_str=data_text[start:end]
    data=json.loads(data_str)['data']
    video_title=data['video']['title']
    print(video_title)

    stream=data['stream']
    mp4_list=[]
    for item in stream:
        download_url=item['segs'][0]['cdn_url']
        mp4_list.append(download_url)
        #print(download_url)

    print(mp4_list[-1])
    download_mp4(mp4_list[-1],download_dir,"tudou_video")

def get_js_from_url():
    url='https://video.tudou.com/v/XNDYwODA3MzQ0OA==.html?spm=a2h28.8313461.feed.dvideo'
    cookies='cna=CDT5FYlWrxcCAQFfOLjhX9s0; __ysuid=1578988773054FaX; csrfToken=bwoyg75WAIC2htXOu8yXCp6y; P_ck_ctl=2ACB8500A507317C2DDE9D0931079A2F; __ayvstp=39; __aysvstp=33; isg=BJOTxqe-yTbOqIVpYzbmdhV5Ihe9SCcKcNIKskWwyLLpxLJmzBnDWrsG_DSq_38C'
    cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookies.split("; ")}

    res=requests.get("https://video.tudou.com/v/XNDYwODA3MzQ0OA==.html?spm=a2h28.8313461.feed.dvideo")
    html=str(res.text.encode('utf-8'))
    start=html.find("__INITIAL_STATE__")+len("__INITIAL_STATE__ =")
    end=html.rfind(";")
    data_str=html[start:end].encode('latin-1').decode('unicode_escape')

    print(data_str)
    data=json.loads(data_str)
    print(data["vid"])

def get_tudou_video(url):
    headers={
        "Referer": "https://video.tudou.com/v/XNDQxOTgwODEyMA==.html?spm=a2h28.8313461.feed.dvideo",
        "Sec-Fetch-Mode": "no-cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }

    cookies='cna=CDT5FYlWrxcCAQFfOLjhX9s0; __ysuid=1578988773054FaX; csrfToken=bwoyg75WAIC2htXOu8yXCp6y; P_ck_ctl=2ACB8500A507317C2DDE9D0931079A2F; __ayvstp=39; __aysvstp=33; isg=BJOTxqe-yTbOqIVpYzbmdhV5Ihe9SCcKcNIKskWwyLLpxLJmzBnDWrsG_DSq_38C'
    cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookies.split("; ")}

    res=requests.get(url,headers=headers,stream=True,cookies=cookie_dict)
    with open(r"F:\study_project\webpack\scrapy\tudou_video\wxw.mp4","wb+") as f:
        f.write(res.content)

def get_fenghuang():

    
    url='https://v.ifeng.com/c/7vTgYVVsCzj'
    res=requests.get(url)
    html=str(res.text.encode('utf-8'))
    start=html.find("var allData")+len("var allData = ")
    end=html.find("var adData")
    target=html.rfind(";",start,end)
    data_str=html[start:target].encode('latin-1').decode('unicode_escape')
    data=json.loads(data_str)
    docData=data['docData']

    title=docData['title']
    mp4=docData['videoPlayUrl']
    m3u8=docData['m3u8Url']

    download_mp4(mp4,download_dir,"denghuang_video")

 


if __name__ == "__main__":

    
    # url='http://47.105.29.43/6974F488A964671CFEF913F39/03000A01005DBA780B06AF9456532BBA2B2795-5E2F-4CCF-8F93-72485C8DD195.mp4?ccode=050F&amp;duration=185&amp;expire=18000&amp;psid=f08edc02727c3e175d568fbbaa5c5140&amp;ups_client_netip=015f221b&amp;ups_ts=1586321620&amp;ups_userid=&amp;utid=tEYUF%2FSgvg8CAQFfIhtZ74Zk&amp;vid=XNDQxOTgwODEyMA%3D%3D&amp;vkey=B3e0a457ff50a144b7a438e66dc7aae86&amp;eo=1&amp;bc=2&amp;dre=u21&amp;si=42&amp;dst=1&ali_redirect_domain=ykugc.cp31.ott.cibntv.net&ali_redirect_ex_ftag=822b18c9ad4fa849a6ee3c590bb272e1f584e5f5ca924ea5&ali_redirect_ex_tmining_ts=1586323943&ali_redirect_ex_tmining_expire=3600&ali_redirect_ex_hot=0'
    # get_tudou_video(url)
    # get_js_from_url()
    # get_mp4_from_js()
    # get_first_url()

    souhuo_download()

   




