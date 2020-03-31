package com.xiaowei.crawl.basic;

import com.xiaowei.crawl.entity.VideoInfo;
import com.xiaowei.crawl.utils.FileUrlDownloadUtil;
import com.xiaowei.crawl.utils.HttpRequest;
import com.xiaowei.crawl.utils.ParsePageUtil;
import lombok.SneakyThrows;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Pattern;

/**
 * Created with IntelliJ IDEA.
 * User：modderBUG
 * Date：2020/3/3015:42
 * Version:1.0
 * Desc:
 */
public class MyCrawler {
    public static void main(String[] args) {
        String downloadDir = "F:/study_project/webpack/scrapy/acfun_video/";  //注意一定加上/

        int VIDEO_QUALITY = 0;  //0是最高.3是最低。
        int userId = 11039293;  //输入用户id爬取全部视频。默认为0

        int DownloadDelay=1000;     //每次下载休息1s
        int MAX_THREAD=5;           //最大线程

        boolean USE_PROXIES=false;  //使用代理,在根目录的proxy.txt添加代理。按照规则添加

        /**
         * @Varb urls 是一个acid(https://www.acfun.cn/v/ac14297460)的列表集合。
         * 可以从排行榜获取，也可以手动添加。下面有演示。
         * */
        HashSet<String> urls = new HashSet<String>();
        //1. 从排行榜获取。rankLimit=3参数是取前三名。
//        urls = HttpRequest.getAcids("https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=&subChannelId=&rankLimit=3&rankPeriod=DAY");

        //2. 手动添加。随便找了几个短视频测试了一下。
        urls.add("https://www.acfun.cn/v/ac14297460");
        urls.add("https://www.acfun.cn/v/ac14134176");
        urls.add("https://www.acfun.cn/v/ac14049069");
        urls.add("https://www.acfun.cn/v/ac13845267");

        //3. 从用户投稿爬取。给上面的userId填写用户id
        if (userId != 0) {
            urls = HttpRequest.getAcidsFromUser("https://www.acfun.cn/space/next?uid=" + userId + "&type=video&orderBy=2&pageNo=", 1);
        }


        List<HashMap<String,String>> proxies=new LinkedList<HashMap<String, String>>();
        try {
            proxies=FileUrlDownloadUtil.getALLProxies("proxy.txt");
        } catch (IOException e) {
            e.printStackTrace();
        }
        ExecutorService fixedThreadPool = Executors.newFixedThreadPool(MAX_THREAD);
        for (String url : urls) {

            if(!USE_PROXIES){
                fixedThreadPool.execute(new CrawlerThread(url, downloadDir, VIDEO_QUALITY,DownloadDelay));
            }else {
                fixedThreadPool.execute(new CrawlerThread(url, downloadDir, VIDEO_QUALITY,DownloadDelay,proxies));
            }

        }
        fixedThreadPool.shutdown();
        while (!fixedThreadPool.isTerminated()) {
            try {
                Thread.sleep(10000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }


        System.out.println("主线程执行完毕！");
    }
}


class CrawlerThread implements Runnable {
    String URL;
    String downloadDir;
    int VIDEO_QUALITY;
    int DownloadDelay;
    List<HashMap<String,String>> proxies;

    CrawlerThread(String url, String downloadDir, int VIDEO_QUALITY,int DownloadDelay) {
        this.URL = url;
        this.downloadDir = downloadDir;
        this.VIDEO_QUALITY = VIDEO_QUALITY;
        this.DownloadDelay=DownloadDelay;
    }
    CrawlerThread(String url, String downloadDir, int VIDEO_QUALITY,int DownloadDelay,List<HashMap<String,String>> proxies) {
        super();
        this.proxies=proxies;
    }

    @SneakyThrows
    public void run() {
        VideoInfo video = ParsePageUtil.getFileDownloadUrls(URL);
        final File file = new File(downloadDir + video.title.replaceAll("[\\pP\\p{Punct}]", ""));
        if (!file.exists()) {
            file.mkdir();
        }

        //清晰度获取,目标视频清晰度可能不存在。于是降级。
        String url = video.getUrls().get(VIDEO_QUALITY);
        while (url == null) {
            url = video.getUrls().get(VIDEO_QUALITY - 1);
        }
        String res = HttpRequest.sendGet(url);

        String[] text = res.split(",");
        List<Thread> tasks = new LinkedList<Thread>();
        for (int i = 1; i < text.length; i++) {
            String video_chip = text[i].split("#")[0];
            final String api = "https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/segment/" + video_chip;
            final int finalI = i;
            Thread a = new Thread(new Runnable() {
                public void run() {
                    if (!proxies.isEmpty()){
                        FileUrlDownloadUtil.downloadFile(api, file.getPath(), "/" + String.format("%04d", finalI) + ".ts", "GET",proxies);
                    }else {
                        FileUrlDownloadUtil.downloadFile(api, file.getPath(), "/" + String.format("%04d", finalI) + ".ts", "GET");
                    }
                }
            });
            a.start();
            tasks.add(a);
        }
        for (Thread item : tasks) {
            item.join();
        }

        if (!URL.contains("_")) {
            ParsePageUtil.mergeDownloadFiles(file.getPath(), video.getVideoList().get(0).get("title").toString().replaceAll("[\\pP\\p{Punct}]", "_") + ".mp4");
        } else {
            int p = Integer.parseInt(URL.split("_")[1]) - 1;
            ParsePageUtil.mergeDownloadFiles(file.getPath(), video.getVideoList().get(p).get("title").toString().replaceAll("[\\pP\\p{Punct}]", "_") + ".mp4");
        }

        Thread.sleep(DownloadDelay);

        if (video.videoList.size() >= 2 && !URL.contains("_")) {
            for (int i = 2; i <= video.videoList.size(); i++) {
                CrawlerThread thread = new CrawlerThread(URL + "_" + i, downloadDir, VIDEO_QUALITY,DownloadDelay,proxies);
                Thread thread1 = new Thread(thread);
                thread1.start();
                thread1.join();
            }
        }

    }
}
