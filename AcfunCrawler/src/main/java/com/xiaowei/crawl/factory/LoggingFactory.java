package com.xiaowei.crawl.factory;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Created with IntelliJ IDEA.
 * User：modderBUG
 * Date：2020/4/216:28
 * Version:1.0
 * Desc:
 */
public class LoggingFactory {
    private volatile static LoggingFactory instance;

    private static CopyOnWriteArrayList<String> logInfo = new CopyOnWriteArrayList<>();
    private static SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置日期格式

    private LoggingFactory() throws IOException {
        File logFile = new File("logging.log");
        if (!logFile.exists()) {
            logFile.createNewFile();
        }
        FileWriter fw = new FileWriter(logFile, true);
        fw.write("\r\n" + df.format(new Date()) + "：-----------------------------工厂开始运行----------------------------\r\n");
        fw.close();
    }

    public void close() throws IOException {
        File logFile = new File("logging.log");
        FileWriter fw = new FileWriter(logFile, true);
        logInfo.forEach(s -> {
            try {
                fw.write(s+ "\r\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
        fw.write(df.format(new Date())+"-----------------------------主线程退出----------------------------\r\n");
        fw.close();
    }

    public static void warning(String str) {
        logInfo.add(df.format(new Date())+":[WARING]"+str);
    }

    public static void info(String str) {
        logInfo.add(df.format(new Date())+ ":[INFO]"+str);
    }

    public static LoggingFactory getInstance()  {
        if (instance == null) {
            synchronized (LoggingFactory.class) {
                if (instance == null) {
                    try {
                        instance = new LoggingFactory();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        return instance;
    }
}
