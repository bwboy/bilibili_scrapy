package com.xiaowei.crawl.basic;

import com.xiaowei.crawl.entity.VideoInfo;
import com.xiaowei.crawl.factory.LoggingFactory;
import com.xiaowei.crawl.factory.MySqlSessionFactory;
import com.xiaowei.crawl.middleware.DownloadMiddleware;
import com.xiaowei.crawl.utils.FileUrlDownloadUtil;
import com.xiaowei.crawl.utils.HttpRequest;
import com.xiaowei.crawl.utils.ParsePageUtil;
import lombok.SneakyThrows;

import java.io.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.Pattern;

/**
 * Created with IntelliJ IDEA.
 * User：modderBUG
 * Date：2020/3/3015:42
 * Version:1.0
 * Desc:
 */
public class MyCrawler {
    public static void main(String[] args) throws IOException {
        Properties properties=getPropertys("");
        LoggingFactory logger=LoggingFactory.getInstance();


        String downloadDir = properties.getProperty("downloadDir").endsWith("/")?properties.getProperty("downloadDir"):properties.getProperty("downloadDir")+"/";  //注意一定加上/

        int VIDEO_QUALITY = Integer.parseInt(properties.getProperty("VIDEO_QUALITY"));  //0是最高.3是最低。
        int userId = Integer.parseInt(properties.getProperty("userId"));  //输入用户id爬取全部视频。默认为0

        int DownloadDelay = Integer.parseInt(properties.getProperty("DownloadDelay"));     //每次下载休息1s
        int MAX_THREAD = Integer.parseInt(properties.getProperty("MAX_THREAD"));           //最大线程

        boolean USE_PROXIES = Boolean.parseBoolean(properties.getProperty("USE_PROXIES"));   //使用代理,在根目录的proxy.txt添加代理。按照规则添加
        boolean USE_HEADERS = Boolean.parseBoolean(properties.getProperty("USE_HEADERS")); ;

        String COOKIES = properties.getProperty("COOKIES");  //使用cookies 格式bili_jct=cbe0b9313c383c280f27e4bbe42ca426; PVID=1; CURRENT_QUALITY=80; bp_t_offset_8960710=371785417260041514; INTVER=1

        /**
         * @Varb urls 是一个acid(https://www.acfun.cn/v/ac14297460)的列表集合。
         * 可以从排行榜获取，也可以手动添加。下面有演示。
         * */
        HashSet<String> urls = new HashSet<String>();
        //1. 从排行榜获取。rankLimit=3参数是取前三名。
//        urls = HttpRequest.getAcids("https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=&subChannelId=&rankLimit=3&rankPeriod=DAY");

        //2. 手动添加。随便找了几个短视频测试了一下。
        urls.add("https://www.acfun.cn/v/ac14366434");
        urls.add("https://www.acfun.cn/v/ac14370533");
//        urls.add("https://www.acfun.cn/v/ac14362609");

        //3. 从用户投稿爬取。给上面的userId填写用户id
        if (userId != 0) {
            urls = HttpRequest.getAcidsFromUser("https://www.acfun.cn/space/next?uid=" + userId + "&type=video&orderBy=2&pageNo=", 1);
        }


        List<HashMap<String, String>> proxies = new LinkedList<HashMap<String, String>>();
        LinkedList<HashMap<String, String>> headers = new LinkedList<>();

        if (!USE_PROXIES) {
            try {
                proxies = FileUrlDownloadUtil.getALLProxies("proxy.txt");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (!USE_HEADERS) {
            try {
                headers = FileUrlDownloadUtil.getALLProxies("headers.txt");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        if (urls.size()>256){
            System.out.println("要下载的视频大于256个，任务队列会被占满！");
        }
        ExecutorService threadPool = new ThreadPoolExecutor(3,
                MAX_THREAD,
                3,
                TimeUnit.SECONDS,
                new LinkedBlockingDeque<>(256),
                Executors.defaultThreadFactory(),
                new ThreadPoolExecutor.CallerRunsPolicy());
        for (String url : urls) {
            threadPool.execute(new CrawlerThread(url, downloadDir, VIDEO_QUALITY, DownloadDelay, proxies, COOKIES));
            try {
                Thread.sleep(DownloadDelay);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        threadPool.shutdown();
        while (!threadPool.isTerminated()) {
            try {
                Thread.sleep(10000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        MySqlSessionFactory.getInstance().close();
        logger.close();
        System.out.println("主线程执行完毕！");
    }

    public   static Properties getPropertys(String fileName)  throws IOException {
        String file=fileName.equals("")?"config.properties":fileName;
        Properties properties = new Properties();
        // 使用InPutStream流读取properties文件
        File propFile=new File(file);
        if (!propFile.exists()){
            propFile.createNewFile();
            FileWriter fw=new FileWriter(propFile);
            fw.write("downloadDir=F:/study_project/webpack/scrapy/acfun_video/\r\n");
            fw.write("VIDEO_QUALITY=3\r\n");
            fw.write("userId=0\r\n");
            fw.write("DownloadDelay=1000\r\n");
            fw.write("MAX_THREAD=5\r\n");
            fw.write("USE_PROXIES=false\r\n");
            fw.write("USE_HEADERS=false\r\n");
            fw.write("COOKIES=\r\n");
            fw.close();
        }
        BufferedReader bufferedReader = new BufferedReader(new FileReader(propFile));
        properties.load(bufferedReader);
        return  properties;
    }
}


class CrawlerThread implements Runnable {
    String URL;
    String downloadDir;
    int VIDEO_QUALITY;
    int DownloadDelay;
    List<HashMap<String, String>> proxies = new LinkedList<HashMap<String, String>>();
    ExecutorService threadPool = new ThreadPoolExecutor(3,
            5,
            3,
            TimeUnit.SECONDS,
            new LinkedBlockingDeque<>(256),
            Executors.defaultThreadFactory(),
            new ThreadPoolExecutor.CallerRunsPolicy());
    String cookies;


    CrawlerThread(String url, String downloadDir, int VIDEO_QUALITY, int DownloadDelay) {
        this.URL = url;
        this.downloadDir = downloadDir;
        this.VIDEO_QUALITY = VIDEO_QUALITY;
        this.DownloadDelay = DownloadDelay;
    }

    CrawlerThread(String url, String downloadDir, int VIDEO_QUALITY, int DownloadDelay, List<HashMap<String, String>> proxies) {
        this(url, downloadDir, VIDEO_QUALITY, DownloadDelay);
        this.proxies = proxies;
    }

    CrawlerThread(String url, String downloadDir, int VIDEO_QUALITY, int DownloadDelay, String cookies) {
        this(url, downloadDir, VIDEO_QUALITY, DownloadDelay);
        this.cookies = cookies;
    }

    CrawlerThread(String url, String downloadDir, int VIDEO_QUALITY, int DownloadDelay, List<HashMap<String, String>> proxies, String cookies) {
        this(url, downloadDir, VIDEO_QUALITY, DownloadDelay);
        this.cookies = cookies;
        this.proxies = proxies;
    }

    @SneakyThrows
    public void run() {
        VideoInfo video = ParsePageUtil.getFileDownloadUrls(URL);

        final File file = new File(downloadDir + video.title.replaceAll("[\\pP\\p{Punct}]", ""));
        if (!file.exists()) {
            file.mkdir();
        }
        video.fileContent = file.getPath();
        ParsePageUtil.saveDate(video);

        //清晰度获取,目标视频清晰度可能不存在。于是降级。
        int QUALITY = VIDEO_QUALITY;
        while (QUALITY >= video.getUrls().size()) {
            QUALITY--;
        }
        String url = video.getUrls().get(QUALITY);
        String res = HttpRequest.sendGet(url);
        String[] text = res.split(",");
        ExecutorService chipsThreadPool = Executors.newFixedThreadPool(5);
        for (int i = 1; i < text.length; i++) {
            String video_chip = text[i].split("#")[0];
            final String api = "https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/segment/" + video_chip;
            final int finalI = i;
            chipsThreadPool.execute(new Thread(() -> {
                DownloadMiddleware.doDownloadchips(api, file.getPath(), "/" + String.format("%04d", finalI) + ".ts", "GET", proxies, cookies);
            }));
        }
        chipsThreadPool.shutdown();
        while (!chipsThreadPool.isTerminated()) {
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        String fileName;
        if (!URL.contains("_")) {
            fileName = video.getVideoList().get(0).get("title").toString().replaceAll("[\\pP\\p{Punct}]", "_") + ".mp4";
            ParsePageUtil.mergeDownloadFiles(file.getPath(), fileName);
        } else {
            int p = Integer.parseInt(URL.split("_")[1]) - 1;
            fileName = video.getVideoList().get(p).get("title").toString().replaceAll("[\\pP\\p{Punct}]", "_") + ".mp4";
            ParsePageUtil.mergeDownloadFiles(file.getPath(), fileName);
        }

        Thread.sleep(DownloadDelay);
        if (video.videoList.size() >= 2 && !URL.contains("_")) {
            for (int i = 2; i <= video.videoList.size(); i++) {
                threadPool.execute(new CrawlerThread(this.URL + "_" + i, this.downloadDir, this.VIDEO_QUALITY, this.DownloadDelay, this.proxies, cookies));
            }
            threadPool.shutdown();
            while (!threadPool.isTerminated()) {
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }

    }
}
