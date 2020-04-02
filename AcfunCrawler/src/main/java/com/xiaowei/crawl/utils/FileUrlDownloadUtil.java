package com.xiaowei.crawl.utils;


import com.sun.xml.internal.ws.util.StringUtils;
import com.xiaowei.crawl.factory.LoggingFactory;
import com.xiaowei.crawl.factory.ProxiesFactory;

import java.io.*;
import java.net.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class FileUrlDownloadUtil {

    /**
     * 说明：根据指定URL将文件下载到指定目标位置
     *
     * @param urlPath     下载路径
     * @param downloadDir 文件存放目录
     * @return 返回下载文件
     */

    @SuppressWarnings("finally")
    public static File downloadFile(String urlPath, String downloadDir, String filename, String method) {
        String proxy = "127.0.0.1:80";
        return downloadFile(urlPath, downloadDir, filename, method, proxy);
    }

    @SuppressWarnings("finally")
    public static File downloadFile(String urlPath, String downloadDir, String filename, String method, String proxy) {
        List<HashMap<String, String>> proxies = new LinkedList<HashMap<String, String>>();
        String cookies = "";
        if (proxy.contains(":")) {
            HashMap<String, String> a = new HashMap<String, String>();
            a.put("ip", proxy.split(":")[0]);
            a.put("port", proxy.split(":")[1]);
            proxies.add(a);
        } else {
            cookies = proxy;
        }
        return downloadFile(urlPath, downloadDir, filename, method, proxies, cookies);
    }

    @SuppressWarnings("finally")
    public static File downloadFile(String urlPath, String downloadDir, String filename, String method,
                                    List<HashMap<String, String>> proxy, String cookies) {
        File file = null;
        try {

            // 统一资源
            URL url = new URL(urlPath);
            // 连接类的父类，抽象类
            URLConnection urlConnection = null;

            Proxy proxies = ProxiesFactory.getInstance().makeProxies(proxy);
            if (!proxies.address().toString().contains("127.0.0.1")) {
                urlConnection = url.openConnection(proxies);
            } else {
                urlConnection = url.openConnection();
            }

            // http的连接类
            HttpURLConnection httpURLConnection = (HttpURLConnection) urlConnection;

            //设置超时
            httpURLConnection.setConnectTimeout(1000 * 5);
            //设置请求方式，默认是GET
            httpURLConnection.setRequestMethod(method);
            // 设置字符编码
            httpURLConnection.setRequestProperty("Charset", "UTF-8");
            if (!cookies.equals("")) {
                httpURLConnection.setRequestProperty("Cookie", cookies);
            }

            // 打开到此 URL引用的资源的通信链接（如果尚未建立这样的连接）。
            httpURLConnection.connect();
            // 文件大小
            int fileLength = httpURLConnection.getContentLength();

            // 控制台打印文件大小
//            System.out.println("您要下载的文件大小为:" + fileLength / (1024 * 1024) + "MB");

            // 建立链接从请求中获取数据
            URLConnection con = url.openConnection();
            BufferedInputStream bin = new BufferedInputStream(httpURLConnection.getInputStream());
            // 指定文件名称(有需求可以自定义)

            String fileFullName = filename;
//            if (urlPath.contains("=")) {
//                fileFullName = urlPath.substring(urlPath.lastIndexOf("=") + 1);
//            }

            // 指定存放位置(有需求可以自定义)
            String path = downloadDir + File.separatorChar + fileFullName;
            file = new File(path);
            if (file.exists()){
                System.out.println("文件已存在！");
                LoggingFactory.warning("文件已存在！"+path);
                return file;
            }
            // 校验文件夹目录是否存在，不存在就创建一个目录
            if (!file.getParentFile().exists()) {
                file.getParentFile().mkdirs();
            }

            OutputStream out = new FileOutputStream(file);
            int size = 0;
            int len = 0;
            byte[] buf = new byte[2048];
            while ((size = bin.read(buf)) != -1) {
                len += size;
                out.write(buf, 0, size);
                // 控制台打印文件下载的百分比情况
//                System.out.println("下载了-------> " + len * 100 / fileLength + "%\n");
            }
            // 关闭资源
            bin.close();
            out.close();
        } catch (MalformedURLException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            System.out.println("文件下载失败！" + filename);
            LoggingFactory.warning("文件下载失败！" + filename);
            downloadRetry(urlPath, downloadDir, filename, method,
                    proxy, cookies);
        } catch (Exception e) {
            System.out.println("出现错误");
            System.out.println(e);
            LoggingFactory.warning("出现错误"+e);
        } finally {
            return file;
        }

    }

    public static void downloadRetry(String urlPath, String downloadDir, String filename, String method,
                                     List<HashMap<String, String>> proxy, String cookies) {
        int i = 0;
        while (i < 5) {
            try {
                downloadFile(urlPath, downloadDir, filename, method,
                        proxy, cookies);
                System.out.println("文件重试成功！" + filename);
                LoggingFactory.warning("文件重试成功！" + filename);

                break;
            } catch (Exception e) {
                System.out.println("第一次重试失败！");
                LoggingFactory.warning("第一次重试失败！");
            }
            i++;
        }
        System.out.println("重试失败！");
        LoggingFactory.warning("重试失败！");
    }

    /**
     * 说明：根据指定URL将文件下载到指定目标位置
     *
     * @param filePath proxy文件路径
     * @return 代理列表。
     */
    public static LinkedList<HashMap<String, String>> getALLProxies(String filePath) throws IOException {
        LinkedList<HashMap<String, String>> proxies = new LinkedList<HashMap<String, String>>();
        File file = new File(filePath);
        if (!file.exists()) {
            file.createNewFile();
            return proxies;
        }
        BufferedReader br = new BufferedReader(new FileReader(file));
        String str = null;
        while ((str = br.readLine()) != null) {
            if (!str.startsWith("#") && !str.equals("")) {
                HashMap<String, String> proxy = new HashMap<String, String>();
                proxy.put("ip", str.split(":")[0]);
                proxy.put("port", str.split(":")[1]);
                proxies.add(proxy);
            }

        }
        return proxies;
    }

    public static List<String> getHeaders(String filePath) throws IOException {
        List<String> headers = new LinkedList<>();
        File file = new File(filePath);
        if (!file.exists()) {
            file.createNewFile();
            return headers;
        }
        BufferedReader br = new BufferedReader(new FileReader(file));
        String str = null;
        while ((str = br.readLine()) != null) {
            if (!str.startsWith("#") && !str.equals("")) {
                headers.add(str);
            }
        }
        return headers;
    }

    /**
     * 测试
     *
     * @param args
     */
    public static void main(String[] args) {

//        downloadFile("http://pic.ibaotu.com/mp3Watermark_v3/19/45/81/90b6614d19ec063b643edf92682d3f55.mp3",
//                "F:/",
//                "aaaa.mp3",
//                "GET");

//        String s = ":阿的说法\\\\/.&*(阿斯蒂芬阿萨德()/*`~?<|第三发送方式{:。}>-,';][=-!#$%^&*+@\\水电费第三方分";
//        s = s.replaceAll("[\\pP\\p{Punct}]", "");
//        System.out.println(s);
//        HashSet<String> urls = HttpRequest.getAcidsFromUser("https://www.acfun.cn/space/next?uid=11039293&type=video&orderBy=2&pageNo=",1);
//
//        for(String url:urls){
//            System.out.println(url);
//        }

        try {
            getHeaders("headers.txt").forEach(a -> {
                System.out.println(a.split(":")[0] + ":" + a.split(":")[1]);
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
