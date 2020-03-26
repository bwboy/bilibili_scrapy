#coding:utf-8

import urllib
import urllib2
import os,re,sys
import requests
import json
import subprocess




m=0
 
url = 'https://www.bilibili.com/video/av17600853?from=search&seid=14315525695693146901'



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer': 'https://www.bilibili.com/video/av17600853?from=search^&seid=14315525695693146901',
    'Origin': 'https://www.bilibili.com',
}

params = (
    ('e', 'ig8euxZM2rNcNbhzhwdVhoMzhzdVhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNC8xNEVE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==^'),
    ('deadline', '1562133968^'),
    ('gen', 'playurl^'),
    ('nbs', '1^'),
    ('oi', '3659290398^'),
    ('os', 'cosu^'),
    ('platform', 'pc^'),
    ('trid', '5fd0f0bb71b94113babda9dc59275c83^'),
    ('uipk', '5^'),
    ('upsig', '01e98eff2f5db5f51baa8258235d7d30^'),
    ('uparams', 'e,deadline,gen,nbs,oi,os,platform,trid,uipk^'),
    ('mid', '0'),
)


def SixNumber(str_number):
    str_number=str(str_number)
    while(len(str_number)<4):
        str_number='0'+str_number
    return str_number
def down(www):

    global m
    for i in range(0,len(www)):
        try:
            new_name="pic/" + SixNumber(m)+".ts"
            print(new_name)
            m+=1
            if not os.path.exists(new_name):
                request =  urllib2.Request(url=www[i], headers=headers)
                response = urllib2.urlopen(request)
                pic=response.read()
                with open("%s" % new_name, "wb") as f:
                    f.write(pic)
                
        except Exception as e:
            print(e)

    
# 合并视频
def combine_video(title):
    currentVideoPath = os.path.join(sys.path[0], 'pic')  # 当前目录作为下载目录
    #print currentVideoPath
    video_list=os.listdir(currentVideoPath)
    ts_list=[]
    for ts in video_list:
        if ts.split(".")[-1]=="ts":
            ts_list.append(ts)
    #os.chdir(currentVideoPath)
    os.chdir(currentVideoPath)
    if len(video_list) >= 1:
        "ffmpeg -i concat:intermediate1.ts|intermediate2.ts -c copy -bsf:a aac_adtstoasc output.mp4"
        cmd = "ffmpeg" + ' -i ' + " \"concat:"
        for i in ts_list:
            
            if i!=ts_list[-1]:
                
                cmd=cmd+i+"|"
                
            else:
                cmd=cmd+i+"\""
        #title=title.encode(sys.getfilesystemencoding())
        


        cmd=cmd+" -acodec copy -vcodec copy -absf aac_adtstoasc "+title+".mp4"

        
        cmd=cmd.encode(sys.getfilesystemencoding())


        if "?" in cmd:
            cmd=cmd.replace("?","")

        print(os.path.exists(title))

        print(cmd)

        
        if not os.path.exists(title):
            subprocess.call(cmd , shell=True)
            print('[视频合并完成]')
            
        
        #remove(ts_list)
        print('[视频清除完成]')


def main():
    response = requests.get(url, headers=headers, params=params)
    #print response 
    name="text.html"
    #with open(name, "wb") as f:
    #    f.write((response.text).encode("utf-8"))
    reg = re.compile(r'(http://upos-hz-mirrorcosu.acgvideo.com.*?flv.*?uipk&mid=0)')#^http\S*flv\S*uipk&mid=0)
    lt= re.findall(reg,response.text)
    title=re.findall("<title .*?>(.*?)</title>",response.text)

    down(lt)
    combine_video("bilibili")
main()
