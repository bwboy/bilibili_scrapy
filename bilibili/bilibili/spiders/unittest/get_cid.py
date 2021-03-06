import requests
import ssl
import re,os,json

'''
author:吴晓伟
desc：用于测试下载流视频可行性的代码片段。完全使用面向过程编程，便于理解。
'''

download_dir=r'F:/study_project/webpack/scrapy'
url='https://www.bilibili.com/video/BV1me411W7J5'


headers_list = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Cookie': 'SESSDATA=aa15d6af%2C1560734457%2Ccc8ca251', # 登录B站后复制一下cookie中的SESSDATA字段,有效期1个月
    'Host': 'api.bilibili.com'
}

header_download={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Range': 'bytes=0-',  # Range 的值要为 bytes=0- 才能下载完整视频
        'Referer': 'https://api.bilibili.com/x/web-interface/view?aid='+str(98645441),  # 注意修改referer,必须要加的!
        'Origin': 'https://www.bilibili.com',
        'Connection': 'keep-alive',
    }

def get_cid():

    bvid=url.split('/')[-1]
    res_cid=requests.get('https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(bvid),headers=headers_list).json()
    cid_list=[]
    for cid in res_cid['data']:
        cid_list.append(cid['cid'])
    cid=cid_list[0]

    res_aid=requests.get('https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}'.format(cid,bvid),headers=headers_list).json()

    print('|----下载的bvid:{}'.format(bvid))
    aid =res_aid['data']['aid'] #re.search(r'/av(\d+)/*', url).group(1)
    print('|----下载的aid:{}'.format(aid))
    # start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + aid
    # res=requests.get(url=start_url,headers=headers_list).json()
    header_download={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Range': 'bytes=0-',  # Range 的值要为 bytes=0- 才能下载完整视频
        'Referer': 'https://api.bilibili.com/x/web-interface/view?aid='+str(aid),  # 注意修改referer,必须要加的!
        'Origin': 'https://www.bilibili.com',
        'Connection': 'keep-alive',
    }
    res=res_aid
    cid=res['data']['cid']
    img_pic=res['data']['pic']
    pages=res['data']['pages']
    author=res['data']['owner']['name']
    video_title=res['data']['title']
    quality=112
    print('|----下载的cid:{}'.format(res['data']['cid']))
    print('|----下载的共有分P数量:{}'.format(len(pages)))
    url_api = 'https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn={}'.format(cid, aid, quality)
    cookies="_uuid=0715C416-F92F-A735-DF6F-0F2BD783455047778infoc; buvid3=C9B613A0-3880-4608-A241-6AD5005980C2155822infoc; LIVE_BUVID=AUTO6515677694765891; sid=9ko0uxh4; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(kJ|u~YlY0J'ulY~~)muRY; im_notify_type_8960710=0; laboratory=1-1; DedeUserID=8960710; DedeUserID__ckMd5=981589d104b0b8cd; SESSDATA=86c82358%2C1599226669%2C7db74*31; bili_jct=cbe0b9313c383c280f27e4bbe42ca426; CURRENT_QUALITY=80; PVID=4; bp_t_offset_8960710=377193884892598175"
    cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookies.split("; ")}
    res=requests.get(url=url_api,headers=header_download,cookies=cookie_dict).json()
    video_list=[]
    for item in res['data']['durl']:
        video_list.append(item['url'])
    #print('|----下载的url_cid:{}'.format(start_url))
    # print('|----下载的url_cid:{}'.format(res_aid))

    print('|----下载的质量:{}'.format(res['data']['quality']))

    print('|----下载的url_list:{}'.format(url_api))
    print('|----列表长度:{}'.format(len(video_list)))
    print('|----下载的视频列表:{}'.format(video_list))
    print('|----开始下载"{}"作者的视频"{}"'.format(author,video_title))

    
    # for video_url in video_list:
    #     response_stream=requests.get(url=video_url,headers=header_download,stream=True)

    #     if not os.path.exists(download_dir+'/{}'.format(video_title)):
    #         os.mkdir(download_dir+'/{}'.format(video_title))
    #     download_img(img_pic,download_dir,video_title)
    #     download_video(video_url,header_download,download_dir,video_title)
    #     with open("{}/{}/{}.mp4".format(download_dir,video_title,video_title),'wb+') as f:
    #         f.write(response_stream.content)
  

    # print("下载完成：{}".format(video_title))

''' 测试requests 分段下载视频数据 每个数据块1024 '''
def download_video(video_url,header_download,download_dir,video_title):
    response_stream=requests.get(url=video_url,headers=header_download,stream=True)
    f = open("{}/{}/{}-2.mp4".format(download_dir,video_title,video_title),'wb+')
    for chunk in response_stream.iter_content(chunk_size=1024):# 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
        if chunk:
            f.write(chunk)
    f.close()



''' 测试requests 下载图像  '''
def download_img(img_url,download_dir,video_title):
    response_stream=requests.get(url=img_url,stream=True)
    with open("{}/{}/{}.{}".format(download_dir,video_title,video_title,img_url.split('.')[-1]),'wb+') as f:
        f.write(response_stream.content)
        f.close()

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
    if not os.path.exists(download_dir+'/{}'.format("每天一遍")):
        os.mkdir(download_dir+'/{}'.format("每天一遍"))
    # download_video("http://upos-sz-mirrorks3.bilivideo.com/upgcxcode/66/93/168389366/168389366-1-30011.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1585319158&gen=playurl&os=ks3bv&oi=23011867&trid=cf24fa2321d848e59ddadf14f49e4bddu&platform=pc&upsig=d887ae15b389e9a7262af5c85b152e94&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&logo=40000000",
    # header_download,
    # download_dir,
    # "每天一遍"

    # )
    get_cid()
    #aaaa()
    # jsontest()