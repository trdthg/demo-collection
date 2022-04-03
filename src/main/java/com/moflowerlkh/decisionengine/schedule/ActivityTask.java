package com.moflowerlkh.decisionengine.schedule;

import com.moflowerlkh.decisionengine.controller.ActivityController;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.Set;

@Service
@EnableScheduling
public class ActivityTask {

    @Autowired
    StringRedisTemplate stringRedisTemplate;

    // 1s
    @Scheduled(fixedDelay = 1000)
    public void task() {
        // activityID -> startTime
        Set<String> activity = stringRedisTemplate.keys(ActivityController.ScheduleKey);
        activity.forEach(item -> {
            String timeStamp = stringRedisTemplate.opsForValue().get(item);
            Date date = new Date(Long.parseLong(timeStamp));
            if (date.getTime() > new Date().getTime()) {
                // generate rand num
                // save to redis
                // send to ms
            }
            // delete redis key
        });
    }
}
