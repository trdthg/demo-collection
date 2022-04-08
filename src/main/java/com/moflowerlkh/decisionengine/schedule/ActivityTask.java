package com.moflowerlkh.decisionengine.schedule;

import com.moflowerlkh.decisionengine.controller.ActivityController;
import com.moflowerlkh.decisionengine.domain.dao.LoanActivityDao;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.service.LoanActivityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.Set;
import java.util.UUID;

@Component
public class ActivityTask {

    @Autowired
    StringRedisTemplate stringRedisTemplate;
    @Autowired
    LoanActivityDao loanActivityDao;

    public static final String ACTIVITY_RANDOM_KEY = "MS_GOODS_RANDOM_KEY";

    // 1s
    @Scheduled(fixedRate = 1000)
    public void task() {
        // activityID -> startTime
        Set<String> activityKeys = stringRedisTemplate.keys(LoanActivityService.ScheduleKey + ".*");
        // System.out.println("定时任务 " + activityKeys);
        if (activityKeys == null) {
            return;
        }
        activityKeys.forEach(key -> {
            String timeStamp = stringRedisTemplate.opsForValue().get(key);
            if (timeStamp == null) {
                return;
            }
            Date date = new Date(Long.parseLong(timeStamp));
            System.out.println("存的时间" + date.getTime() + "   现在" + new Date().getTime());
            if (date.getTime() < new Date().getTime()) {
                String activityId = key.replace(LoanActivityService.ScheduleKey + ".", "");
                System.out.println(activityId);
                LoanActivity loanActivity = loanActivityDao.findById(Long.valueOf(activityId))
                        .orElseThrow(() -> new RuntimeException("fuck you"));
                stringRedisTemplate.opsForValue().set(ACTIVITY_RANDOM_KEY + "." + loanActivity.getGoodsId(),
                        UUID.randomUUID().toString());
                stringRedisTemplate.delete(key);
            }
            // delete redis key
        });
    }
}
