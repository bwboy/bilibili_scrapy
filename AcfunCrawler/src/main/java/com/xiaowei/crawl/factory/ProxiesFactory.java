package com.xiaowei.crawl.factory;

import java.net.InetSocketAddress;
import java.net.Proxy;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Random;

/**
 * Created with IntelliJ IDEA.
 * User：modderBUG
 * Date：2020/3/3118:50
 * Version:1.0
 * Desc:
 */
public class ProxiesFactory {

        public Proxy makeProxies(List<HashMap<String,String> > proxies) {

            HashMap<String,String> proxy = proxies.get(new Random().nextInt(proxies.size()+1));

            InetSocketAddress addr = new InetSocketAddress(proxy.get("ip"), Integer.parseInt(proxy.get("port")));

            return new Proxy(Proxy.Type.HTTP, addr); // http 代理
        }
    public static void main(String[] args) {

    }

}
