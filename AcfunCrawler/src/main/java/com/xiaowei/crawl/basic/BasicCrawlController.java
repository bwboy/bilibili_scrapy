/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 * <p>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.xiaowei.crawl.basic;

import com.xiaowei.crawl.utils.HttpRequest;
import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashSet;

/**
 * @author Yasser Ganjisaffar
 */
public class BasicCrawlController {
    private static final Logger logger = LoggerFactory.getLogger(BasicCrawlController.class);

    public static void main(String[] args) throws Exception {
//        if (args.length != 2) {
//            logger.info("Needed parameters: ");
//            logger.info("\t rootFolder (it will contain intermediate crawl data)");
//            logger.info("\t numberOfCralwers (number of concurrent threads)");
//            return;
//        }

        /*
         * crawlStorageFolder is a folder where intermediate crawl data is
         * stored.
         * numberOfCrawlers shows the number of concurrent threads that should
         * be initiated for crawling.
         * numberOfCrawlers 显示应启动进行爬网的并发线程数。
         * crawlStorageFolder是存储中间爬网数据的文件夹。
         */
        String crawlStorageFolder = "F:/study_project/webpack/scrapy/acfun_video/"; //args[0];
        int numberOfCrawlers = 5; //Integer.parseInt(args[1]);

        CrawlConfig config = new CrawlConfig();
        config.setUserAgentString("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36");
        config.setIncludeHttpsPages(true);
        config.setCrawlStorageFolder(crawlStorageFolder);

        /*
         * Be polite: Make sure that we don't send more than 1 request per
         * second (1000 milliseconds between requests).
         * 要礼貌：确保我们每秒发送的请求不超过1个（两次请求之间的间隔为1000毫秒）。
         */
        config.setPolitenessDelay(1000);

        /*
         * You can set the maximum crawl depth here. The default value is -1 for
         * unlimited depth
         * 您可以在此处设置最大爬网深度。 默认值是-1，表示无限深度
         */
        config.setMaxDepthOfCrawling(2);

    /*
     * You can set the maximum number of pages to crawl. The default value
     * is -1 for unlimited number of pages
     * You can set the maximum number of pages to crawl. The default value is -1 for unlimited number of pages
     * 您可以设置要爬网的最大页面数。 默认值是-1，表示无限制的页面数
   * 您可以设置要爬网的最大页面数。 默认值是-1，表示无限制的页面数
     */
        config.setMaxPagesToFetch(1000);

        /**
         * Do you want crawler4j to crawl also binary data ?
         * example: the contents of pdf, or the metadata of images etc
         * 您是否希望crawler4j还能对二进制数据进行爬网？ 例如：pdf的内容或图像的元数据等
         */
        config.setIncludeBinaryContentInCrawling(true);

        /*
         * Do you need to set a proxy? If so, you can use:
         * 您需要设置代理吗？ 如果是这样，您可以使用：
         * config.setProxyHost("proxyserver.example.com");
         * config.setProxyPort(8080);
         *
         * If your proxy also needs authentication:
         * config.setProxyUsername(username); config.getProxyPassword(password);
         */

        /*
         * This config parameter can be used to set your crawl to be resumable
         * (meaning that you can resume the crawl from a previously
         * interrupted/crashed crawl). Note: if you enable resuming feature and
         * want to start a fresh crawl, you need to delete the contents of
         * rootFolder manually.
         * 此配置参数可用于将爬网设置为可恢复（意味着您可以从先前中断/崩溃的爬网中恢复爬网）。 注意：如果启用了恢复功能并想开始全新的爬网，则需要手动删除rootFolder的内容。
         */
        config.setResumableCrawling(false);

        /*
         * Instantiate the controller for this crawl.
         * 实例化此爬网的控制器。
         */
        PageFetcher pageFetcher = new PageFetcher(config);
        RobotstxtConfig robotstxtConfig = new RobotstxtConfig();



        robotstxtConfig.setUserAgentName("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36");
        RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
        CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);

        /*
         * For each crawl, you need to add some seed urls. These are the first
         * URLs that are fetched and then the crawler starts following links
         * which are found in these pages
         * 对于每个爬网，您需要添加一些种子URL。 这些是第一个获取的URL，然后搜寻器开始跟随这些页面中找到的链接
         */

        /**
         * 1.HTTP库访问排行榜api。
         * 2.通过解析获取地址
         * 3.循环添加seed，下载视频。
         * */


        HashSet<String> urls =new HashSet<String>();
        urls=HttpRequest.getAcids("https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=&subChannelId=&rankLimit=3&rankPeriod=DAY");
        for (String url:urls){
            controller.addSeed(url);
        }

//        controller.addSeed("https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=&subChannelId=&rankLimit=30&rankPeriod=DAY");
//        controller.addSeed("https://www.acfun.cn/rank/list/#cid=-1;range=1");
//        controller.addSeed("http://www.ics.uci.edu/~welling/");

        /*
         * Start the crawl. This is a blocking operation, meaning that your code
         * will reach the line after this only when crawling is finished.
         * 开始抓取。 这是一项阻止操作，这意味着仅在完成爬网之后，您的代码才能到达该行。
         */
        controller.start(BasicCrawler.class, numberOfCrawlers);
    }
}