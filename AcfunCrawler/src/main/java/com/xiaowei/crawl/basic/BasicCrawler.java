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

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.google.common.io.Files;
import com.xiaowei.crawl.entity.VideoInfo;
import com.xiaowei.crawl.utils.FileUrlDownloadUtil;
import com.xiaowei.crawl.utils.HttpRequest;
import com.xiaowei.crawl.utils.ParsePageUtil;
import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;
import lombok.SneakyThrows;
import org.apache.http.Header;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.regex.Pattern;

/**
 * @author Yasser Ganjisaffar
 */
public class BasicCrawler extends WebCrawler {

    private static final Pattern IMAGE_EXTENSIONS = Pattern.compile(".*\\.(bmp|gif|jpg|png)$");

    /**
     * You should implement this function to specify whether the given url
     * should be crawled or not (based on your crawling logic).
     * 您应该实现此功能，以指定是否应对给定的url进行爬网（基于您的爬网逻辑）。
     */
    @Override
    public boolean shouldVisit(Page referringPage, WebURL url) {
        String href = url.getURL().toLowerCase();
        // Ignore the url if it has an extension that matches our defined set of image extensions.
        if (IMAGE_EXTENSIONS.matcher(href).matches()) {
            return false;
        }

        // Only accept the url if it is in the "www.ics.uci.edu" domain and protocol is "http".
        // 仅当网址位于“ www.ics.uci.edu”域且协议为“ http”时，才接受该网址。
        return href.contains("acfun.cn");
    }

    /**
     * This function is called when a page is fetched and ready to be processed
     * by your program.
     * 当获取页面并准备好由程序处理时，将调用此函数。
     */
    @SneakyThrows
    @Override
    public void visit(Page page) {

        int docid = page.getWebURL().getDocid();
        String url = page.getWebURL().getURL();
        String domain = page.getWebURL().getDomain();
        String path = page.getWebURL().getPath();
        String subDomain = page.getWebURL().getSubDomain();
        String parentUrl = page.getWebURL().getParentUrl();
        String anchor = page.getWebURL().getAnchor();

//        logger.debug("Docid: {}", docid);
//        logger.info("URL: {}", url);
//        logger.debug("Domain: '{}'", domain);
//        logger.debug("Sub-domain: '{}'", subDomain);
//        logger.debug("Path: '{}'", path);
//        logger.debug("Parent page: {}", parentUrl);
//        logger.debug("Anchor text: {}", anchor);

        if (page.getParseData() instanceof HtmlParseData) {
            HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
            String text = htmlParseData.getText();
            String html = htmlParseData.getHtml();
            Set<WebURL> links = htmlParseData.getOutgoingUrls();

            logger.debug("Text length: {}", text.length());
            logger.debug("Html length: {}", html.length());
            logger.debug("Number of outgoing links: {}", links.size());
        }



//        String m3u_url=ParsePageUtil.getFileDownloadUrls(page.getWebURL().getURL()).get(3);//视频清晰度

        VideoInfo video=ParsePageUtil.getFileDownloadUrls(page.getWebURL().getURL());

        final File file = new File("F:/study_project/webpack/scrapy/acfun_video/" + video.title);
        if (!file.exists()) {
            file.mkdir();

        }

        String res = HttpRequest.sendGet(video.getUrls().get(3));
        String[] text = res.split(",");
        List<Thread> tasks =new LinkedList<Thread>();
        for (int i = 1; i <= text.length; i++) {
            String video_chip = text[i].split("#")[0];
            final String api ="https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/segment/"+video_chip;
            final int finalI = i;
            Thread a =new Thread(new Runnable() {
                public void run() {
                    FileUrlDownloadUtil.downloadFile(api, file.getPath(), "/" + String.format("%04d",finalI) + ".ts", "gGET");
                }
            });
            tasks.add(a);
        }
        for (Thread item : tasks){
            item.join();
        }

        ParsePageUtil.mergeDownloadFiles(file.getPath(),video.getVideoList().get(0).get("title")+".mp4");

         System.out.println("视频合并完成;"+video.getVideoList().get(0).get("title")+".mp4");

        //DecimalFormat df = new DecimalFormat("0000");
        //df.format(1)


//        if (page.getWebURL().getURL().contains("rank")) {
//
//            String text = new String(page.getContentData());
//            JSONObject obj = JSON.parseObject(text);
//            JSONArray arry = (JSONArray) obj.get("rankList");
//            for (Object a : arry) {
//                JSONObject json = (JSONObject) JSON.toJSON(a);
//                String videourl = (String) json.get("shareUrl");
//                System.out.println(videourl);
//            }
//            // store image
//            String filename = "F:/study_project/webpack/scrapy/acfun_video/asd.txt";
//            try {
//                Files.write(page.getContentData(), new File(filename));
//                WebCrawler.logger.info("Stored: {}", url);
//            } catch (IOException iox) {
//                WebCrawler.logger.error("Failed to write file: " + filename, iox);
//            }
//        }


        Header[] responseHeaders = page.getFetchResponseHeaders();
        if (responseHeaders != null) {
            logger.debug("Response headers:");
            for (Header header : responseHeaders) {
                logger.debug("\t{}: {}", header.getName(), header.getValue());
            }
        }

        logger.debug("=============");
    }
}
