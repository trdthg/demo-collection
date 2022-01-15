package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.util.RedisUtil;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;

@Component
public class Sheduled {

    @Resource
    private RedisUtil redisUtil;

    @Scheduled(cron = "0/10 * * * * ?") //每天开始15秒执行一次
    public void test(){
        String s = String.valueOf(redisUtil.get("a"));
        System.out.println(s);
        redisUtil.set("a", String.valueOf(System.currentTimeMillis()));
    }
}
