package com.xiaowei.crawl.basic;

import com.xiaowei.crawl.entity.VideoInfo;
import com.xiaowei.crawl.utils.FileUrlDownloadUtil;
import com.xiaowei.crawl.utils.HttpRequest;
import com.xiaowei.crawl.utils.ParsePageUtil;
import lombok.SneakyThrows;

import java.io.File;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
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
        String downloadDir="F:/study_project/webpack/scrapy/acfun_video/";  //注意一定加上/

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


        List<Thread> tasks = new LinkedList<Thread>();
        for (String url : urls) {
            CrawlerThread thread = new CrawlerThread(url,downloadDir);
            Thread thread1 = new Thread(thread);
            thread1.start();
            tasks.add(thread1);
        }

        for (Thread item : tasks) {
            try {
                item.join();
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

    CrawlerThread(String url,String downloadDir) {
        this.URL = url;
        this.downloadDir=downloadDir;
    }

    @SneakyThrows
    public void run() {

        VideoInfo video = ParsePageUtil.getFileDownloadUrls(URL);

        final File file = new File(downloadDir + video.title.replaceAll("[\\pP\\p{Punct}]", ""));
        if (!file.exists()) {
            file.mkdir();

        }



        String res = HttpRequest.sendGet(video.getUrls().get(3));
        String[] text = res.split(",");
        List<Thread> tasks = new LinkedList<Thread>();
        for (int i = 1; i < text.length; i++) {
            String video_chip = text[i].split("#")[0];
            final String api = "https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/segment/" + video_chip;
            final int finalI = i;
            Thread a = new Thread(new Runnable() {
                public void run() {
                    FileUrlDownloadUtil.downloadFile(api, file.getPath(), "/" + String.format("%04d", finalI) + ".ts", "GET");
                }
            });
            a.start();
            tasks.add(a);
        }
        for (Thread item : tasks) {
            item.join();
        }

        ParsePageUtil.mergeDownloadFiles(file.getPath(), video.getVideoList().get(0).get("title") + ".mp4");


    }
}
