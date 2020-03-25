import requests
import ssl
import re,os,json

'''
author:吴晓伟
desc：用于测试下载流视频可行性的代码片段。完全使用面向过程编程，便于理解。
'''

download_dir=r'F:/study_project/webpack/scrapy'
url='https://www.bilibili.com/video/BV1h7411R7ne'
headers_list = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Cookie': 'SESSDATA=aa15d6af%2C1560734457%2Ccc8ca251', # 登录B站后复制一下cookie中的SESSDATA字段,有效期1个月
    'Host': 'api.bilibili.com'
}

''' 测试requests 分段下载视频数据 每个数据块1024 '''
def download_video(video_url,header_download,download_dir,video_title):
    response_stream=requests.get(url=video_url,headers=header_download,stream=True)
    f = open("{}/{}/{}-2.mp4".format(download_dir,video_title,video_title),'wb+')
    for chunk in response_stream.iter_content(chunk_size=1024):# 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
        if chunk:
            f.write(chunk)
    f.close()


    

download_header={
    "Origin": "https://www.acfun.cn",
"Referer": "https://www.acfun.cn/v/ac14135772",
"Sec-Fetch-Mode": "cors",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}


'''测试下载A站视频流。得到很多.ts视频碎片 '''
def getVideoList():
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
    cookie='_did=web_587276529C71F009; uuid=5761bae80e67081a44e1237dd6b4610a; analytics=GA1.2.322245661.1584677218; ac__avi=1010874449232f551a0a15edb1a4042660b6a2365c641059371cf6c2c6febafe3a364146315ef65213; session_id=8151145309CA9EDE; Hm_lvt_2af69bc2b378fb58ae04ed2a04257ed1=1584677211,1585098768; analytics_gid=GA1.2.1325401876.1585098769; csrfToken=x6A3sEmzYUy5DSog38qERY3y; safety_id=AAKKUhcwT1IltFdY-__D7FH0; webp_supported=%7B%22lossy%22%3Atrue%2C%22lossless%22%3Atrue%2C%22alpha%22%3Atrue%2C%22animation%22%3Atrue%7D; lsv_js_player_v2_main=a91b93; cur_req_id=9361888160117998_self_f02ce542ccbe97bb7865d7eb8089dc0f; cur_group_id=9361888160117998_self_f02ce542ccbe97bb7865d7eb8089dc0f_0; lsv_js_player_v1_main=f2c6e6; Hm_lpvt_2af69bc2b378fb58ae04ed2a04257ed1=1585110433'
    cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}
    url='https://www.acfun.cn/v/ac14135772'
    response=requests.get(url,cookies=cookie_dict,headers=headers)
    josnp=response.text

    s=josnp.find("window.videoInfo =",0)
    e=josnp.find("window.qualityConfig",0)
    s1=josnp.find(";",s,e)
    data=json.loads(josnp[s+len("window.videoInfo ="):s1])
    jsonstr=data['currentVideoInfo']['ksPlayJson']
    video_info_list=json.loads(jsonstr)['adaptationSet']['representation']

    count=0
    for info_item in video_info_list:
        info_item['url']
        download_video2('F:/study_project/webpack/scrapy/acfun_video/{}.m3u8'.format(count),info_item['url'],download_header)
        download_split('F:/study_project/webpack/scrapy/acfun_video/{}.m3u8'.format(count),count)
        count+=1

    #下载完3个m3u8文件。打开3个文件获取下载内容。
''' 测试requests 分段下载视频数据 每个数据块1024 '''
def download_video2(filename,url,headers):
    response_stream=requests.get(url=url,headers=headers,stream=True)
    f = open(filename,'wb+')
    for chunk in response_stream.iter_content(chunk_size=1024):# 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
        if chunk:
            f.write(chunk)
    f.close()

def download_split(filepath,filename):
    with open(filepath,"r",encoding="utf-8") as f:
        videolist=f.read()
    ITEMS=videolist.split(',')[1:]
    count=0
    for item in ITEMS:
        api='https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/segment/'+item.split('#')[0].strip()
        download_video2('F:/study_project/webpack/scrapy/acfun_video/{}-{}.ts'.format(filename,count),api,download_header)
        print("下载地址："+api)
        # print("下载完成！{}".format('F:/study_project/webpack/scrapy/acfun_video/{}-{}.m3u'.format(filename,count)))
        count+=1


    
    

def aaaa():
    res=requests.get('http://pic.ibaotu.com/mp3Watermark_v3/19/45/81/90b6614d19ec063b643edf92682d3f55.mp3')
    with open(download_dir+'/90b6614d19ec063b643edf92682d3f55.mp3','wb+') as f:
        f.write(res.content)

def jsontest():
    a='{"code":0,"message":"0","ttl":1,"data":[{"cid":75096861,"page":1,"from":"vupload","part":"Red Alert 2情怀回顾！","duration":66,"vid":"","weblink":"","dimension":{"width":1600,"height":900,"rotate":0}}]}'
    data=json.loads(a)
    print(data['code'])
    print(data['data'][0]['cid'])

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    getVideoList()
    #get_cid()
    #aaaa()
    # jsontest()