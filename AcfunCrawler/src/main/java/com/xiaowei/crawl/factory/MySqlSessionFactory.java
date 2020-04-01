package com.xiaowei.crawl.factory;



import java.io.InputStream;
import java.io.Reader;
import java.math.BigDecimal;
import java.net.URL;
import java.sql.*;
import java.util.Calendar;


/**
 * Created with IntelliJ IDEA.
 * User：modderBUG
 * Date：2020/4/117:43
 * Version:1.0
 * Desc:
 */
public class MySqlSessionFactory {
    private static MySqlSessionFactory instance;
    private static final String url = "jdbc:mysql://localhost:3306/scrapy01?serverTimezone=Asia/Shanghai&characterEncoding=utf8&useSSL=false";
    private static final String name = "com.mysql.jdbc.Driver";
    private static final String username = "wxwmodder";
    private static final String password = "sxmc321";

    private   Connection connection ;

    PreparedStatement preparedStatement;

    public MySqlSessionFactory(){
        try{
            Class.forName(name);
            connection =  DriverManager.getConnection(url, username, password);
            connection.setAutoCommit(false);
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public void close(){
        try{
            connection.commit();
            this.connection.close();
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    public static MySqlSessionFactory getInstance() {
        if (instance == null) {
            synchronized (MySqlSessionFactory.class) {
                if (instance == null) {
                    instance = new MySqlSessionFactory();
                }
            }
        }
        return instance;
    }


    public  void  addSql(String sql ) throws SQLException {
        preparedStatement= connection.prepareStatement(sql);
        preparedStatement.execute();
    }
    public  void  addSqlToAcfunInfo(String title,
                                    String coverUrl,
                                    String durationMillis,
                                    String currentVideoId,
                                    String viewCount,
                                    String commentCount,
                                    String user,
                                    String bananaCount,
                                    String createTimeMillis,
                                    String likeCount,
                                    String giftPeachCount,
                                    String stowCount,
                                    String shareCount,
                                    String danmakuCount,
                                    String tags,
                                    String classes,
                                    String file_content) throws SQLException {

         String sql="insert into `acfun_info` (title,coverUrl,durationMillis,currentVideoId,viewCount,commentCount,user,bananaCount,createTimeMillis,likeCount,giftPeachCount,stowCount,shareCount,danmakuCount,tags,classes,file_content) values ('"+title+"','"+coverUrl+"','"+durationMillis+"','"+currentVideoId+"','"+viewCount+"','"+commentCount+"','"+user+"','"+bananaCount+"','"+createTimeMillis+"','"+likeCount+"','"+giftPeachCount+"','"+stowCount+"','"+shareCount+"','"+danmakuCount+"','"+tags+"','"+classes+"','"+file_content+"')";
        preparedStatement= connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
        preparedStatement.execute();
    }


    public static void main(String[] args){
        MySqlSessionFactory dbManager = new MySqlSessionFactory();  //实例化
        try{
            dbManager.addSql("insert into `acfun_info` (title,coverUrl,durationMillis,currentVideoId,viewCount,commentCount,user,bananaCount,createTimeMillis,likeCount,giftPeachCount,stowCount,shareCount,danmakuCount,tags,classes,file_content) values ('','',1585664848187,'','','','','',1585664848187,'','','','','','','','file_content')");
            dbManager.close();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}


