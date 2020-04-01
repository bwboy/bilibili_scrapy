package com.xiaowei.crawl.middleware;

import com.xiaowei.crawl.utils.FileUrlDownloadUtil;
import sun.plugin.liveconnect.LiveConnect;

import java.io.File;
import java.util.HashMap;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User：modderBUG
 * Date：2020/4/19:49
 * Version:1.0
 * Desc:
 */
public class DownloadMiddleware {

    public static Boolean doDownloadchips(String urlPath, String downloadDir, String filename, String method,
                                          List<HashMap<String, String>> proxy, String cookies) {
        try {

            if (!proxy.isEmpty() && !cookies.equals("")) {
                FileUrlDownloadUtil.downloadFile(urlPath, downloadDir, filename, method, proxy, cookies);
            }

            if (proxy.isEmpty()) {
                FileUrlDownloadUtil.downloadFile(urlPath, downloadDir, filename, method);
            }

            if (!cookies.equals("")) {
                FileUrlDownloadUtil.downloadFile(urlPath, downloadDir, filename, method, cookies);
            }
        } catch (Exception e) {
            System.out.println(e);
            return false;
        }

        return true;
    }



}
