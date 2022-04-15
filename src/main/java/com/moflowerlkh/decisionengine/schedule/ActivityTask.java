package com.moflowerlkh.decisionengine.schedule;

import com.moflowerlkh.decisionengine.domain.dao.ActivityDao;
import com.moflowerlkh.decisionengine.domain.entities.Activity;
import com.moflowerlkh.decisionengine.service.LoanActivityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.Set;
import java.util.UUID;

@Component
public class ActivityTask {

    @Autowired
    StringRedisTemplate stringRedisTemplate;
    @Autowired
    ActivityDao activityDao;

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

                System.out.println("查询活动对应的 goodid");
                Long goodId;
                Activity activity = activityDao.findById(Long.valueOf(activityId)).orElseThrow(() -> new RuntimeException("没有查询待准备开始的活动"));
                goodId = activity.getGoodsId();
                System.out.println("存储了RANDOM_KEY");
                stringRedisTemplate.opsForValue().set(ACTIVITY_RANDOM_KEY + "." + goodId,
                        UUID.randomUUID().toString());
                stringRedisTemplate.delete(key);
            }
        });
    }
}
