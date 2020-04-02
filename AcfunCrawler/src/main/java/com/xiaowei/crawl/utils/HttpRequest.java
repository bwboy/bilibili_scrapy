package com.xiaowei.crawl.utils;


import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.google.common.io.Files;
import com.xiaowei.crawl.basic.MyCrawler;


import java.io.*;
import java.net.URL;
import java.net.URLConnection;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * @author 吴晓伟
 * Desc:包含
 * 1.发送get请求 和 重载方法
 * 2.发送post请求
 * 3.从排行榜api接口获取acid列表集合。注意是rest形式。
 * 4.从用户投稿取得acid列表集合。
 */
public class HttpRequest {
    /**
     * 向指定URL发送GET方法的请求
     *
     * @param url   发送请求的URL
     * @param param 请求参数，请求参数应该是 name1=value1&name2=value2 的形式。
     * @return URL 所代表远程资源的响应结果
     */
    public static String sendGet(String url, String param) {
        String URL = url + "?" + param;
        return sendGet(URL);
    }


    public static String sendGet(String url) {
        String result = "";
        BufferedReader in = null;
        try {

            URL realUrl = new URL(url);
            // 打开和URL之间的连接
            URLConnection connection = realUrl.openConnection();
            // 设置通用的请求属性
            connection.setRequestProperty("accept", "*/*");
            connection.setRequestProperty("connection", "Keep-Alive");
            connection.setRequestProperty("user-agent",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36");
            // 建立实际的连接
            connection.connect();
            // 获取所有响应头字段
            Map<String, List<String>> map = connection.getHeaderFields();
            // 遍历所有的响应头字段
            for (String key : map.keySet()) {
                System.out.println(key + "--->" + map.get(key));
            }
            // 定义 BufferedReader输入流来读取URL的响应
            in = new BufferedReader(new InputStreamReader(
                    connection.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                result += line;
            }
        } catch (Exception e) {
            System.out.println("发送GET请求出现异常！" + e);
            e.printStackTrace();
        }
        // 使用finally块来关闭输入流
        finally {
            try {
                if (in != null) {
                    in.close();
                }
            } catch (Exception e2) {
                e2.printStackTrace();
            }
        }
        return result;
    }

    /**
     * 向指定 URL 发送POST方法的请求
     *
     * @param url   发送请求的 URL
     * @param param 请求参数，请求参数应该是 name1=value1&name2=value2 的形式。
     * @return 所代表远程资源的响应结果
     */
    public static String sendPost(String url, String param) {
        PrintWriter out = null;
        BufferedReader in = null;
        String result = "";
        try {
            URL realUrl = new URL(url);
            // 打开和URL之间的连接
            URLConnection conn = realUrl.openConnection();
            // 设置通用的请求属性
            conn.setRequestProperty("accept", "*/*");
            conn.setRequestProperty("connection", "Keep-Alive");
            conn.setRequestProperty("user-agent",
                    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)");
            // 发送POST请求必须设置如下两行
            conn.setDoOutput(true);
            conn.setDoInput(true);
            // 获取URLConnection对象对应的输出流
            out = new PrintWriter(conn.getOutputStream());
            // 发送请求参数
            out.print(param);
            // flush输出流的缓冲
            out.flush();
            // 定义BufferedReader输入流来读取URL的响应
            in = new BufferedReader(
                    new InputStreamReader(conn.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                result += line;
            }
        } catch (Exception e) {
            System.out.println("发送 POST 请求出现异常！" + e);
            e.printStackTrace();
        }
        //使用finally块来关闭输出流、输入流
        finally {
            try {
                if (out != null) {
                    out.close();
                }
                if (in != null) {
                    in.close();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
        return result;
    }

    /**
     * 排行榜接口获取acid列表集合。
     *
     * @param url 排行榜api
     * @return 全部acid列表的url集合。
     */
    public static HashSet<String> getAcids(String url) {
        HashSet<String> urls = new HashSet<String>();
        String text = new String(HttpRequest.sendGet(url));
        JSONObject obj = JSON.parseObject(text);
        JSONArray arry = (JSONArray) obj.get("rankList");
        for (Object a : arry) {
            JSONObject json = (JSONObject) JSON.toJSON(a);
            String videourl = (String) json.get("shareUrl");
            urls.add(videourl);
            System.out.println(videourl);
        }
        // store image
        String filename = "F:/study_project/webpack/scrapy/acfun_video/asd.txt";
        try {
            Files.write(text.getBytes(), new File(filename));

        } catch (IOException iox) {

        }
        return urls;
    }


    /**
     * 从用户投稿取得acid列表集合。
     *
     * @param url     用户投稿api
     * @param pageNum 第几页。
     * @return 全部acid列表的url集合。
     */
    public static HashSet<String> getAcidsFromUser(String url, Integer pageNum) {
        String fullurl = url + pageNum;
        HashSet<String> urls = new HashSet<String>();
        JSONObject obj = JSONObject.parseObject(HttpRequest.sendGet(fullurl));
        JSONObject data = (JSONObject) obj.get("data");
        JSONObject page = (JSONObject) data.get("page");
        String str = data.get("html").toString();
        Pattern pattern = Pattern.compile("/v/ac[1-9][0-9]{4,}");
        Matcher matcher = pattern.matcher(str);

        while (matcher.find()) {
            urls.add("https://www.acfun.cn" + matcher.group());
        }

        if (pageNum == 1) {
            int totalPage = Integer.parseInt(page.get("totalPage").toString());
            if (totalPage >= 2) {
                for (int i = 2; i <= totalPage; i++) {
                    HashSet<String> page_urls = getAcidsFromUser(url, i);
                    urls.addAll(page_urls);
                }
            }
        }
        return urls;
    }


    public static void main(String[] args) {
//        //发送 GET 请求
//        String s=HttpRequest.sendGet("http://localhost:6144/Home/RequestString", "key=123&v=456");
//        System.out.println(s);
//
//        //发送 POST 请求
//        String sr=HttpRequest.sendPost("http://localhost:6144/Home/RequestPostString", "key=123&v=456");
//        System.out.println(sr);

//        HashSet<String> a =new HashSet<String>();
//        a=HttpRequest.getAcids("https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=&subChannelId=&rankLimit=30&rankPeriod=DAY");

//        ExecutorService threadPool = new ThreadPoolExecutor(3,
//                5,
//                3,
//                TimeUnit.SECONDS,
//                new LinkedBlockingDeque<>(50),
//                Executors.defaultThreadFactory(),
//                new ThreadPoolExecutor.CallerRunsPolicy());
//        for (int i = 0; i < 5; i++) {
//            threadPool.execute(() -> {
//                try {
//                    TimeUnit.SECONDS.sleep(3);
//                } catch (InterruptedException e) {
//                    e.printStackTrace();
//                }
//                System.out.println("执行完成"+Thread.currentThread().getName());
//            });
//        }

//        Properties properties= null;
//        try {
//            properties = MyCrawler.getPropertys("");
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//
//        // 获取key对应的value值
//        properties.getProperty("downloadDir");
//
//        System.out.println("a"+ properties.getProperty("COOKIES")+"b");

        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置日期格式
        ConcurrentHashMap<String,String> a=new ConcurrentHashMap<>();

        CopyOnWriteArrayList<String> b = new CopyOnWriteArrayList<>();

        for (int i = 0; i <100 ; i++) {
            new Thread(()->{
                b.add(df.format(new Date())+"aaaaaa");
            }).start();
        }

        b.forEach(s->{
            System.out.println(s+"");
        });

    }
}