package com.moflowerlkh.decisionengine.component;

import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.enums.Gender;
import com.moflowerlkh.decisionengine.util.RedisUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import java.util.List;

@Component
public class Sheduled {

    @Resource
    private RedisUtil redisUtil;

    @Autowired
    UserDao userDao;

    @Scheduled(cron = "0/30 * * * * ?") //每天开始15秒执行一次
    public void testRedis(){
        String s = String.valueOf(redisUtil.get("a"));
        System.out.println(s);
        redisUtil.set("a", String.valueOf(System.currentTimeMillis()));

        System.out.println("A22-redis" + System.currentTimeMillis());
    }

    @Scheduled(cron = "0/30 * * * * ?") //每天开始15秒执行一次
    public void testMysql() {
        List<User> users = userDao.findAll();
        System.out.println(users);
        if (users.isEmpty()) {
            User newUser = new User();
            newUser.setId(112L);
            newUser.setUsername("asd");

            String encodedPassword = new BCryptPasswordEncoder().encode("asd");
            newUser.setPassword(encodedPassword);

            newUser.setYearIncome(10L);
            newUser.setGender(Gender.Male);
            newUser.setAge(18);
            newUser.setName("小明");
            userDao.save(newUser);
        } else {
            users.get(0).setAge(users.get(0).getAge() + 1);
            users.get(0).setPassword(new BCryptPasswordEncoder().encode("asd"));

            userDao.saveAndFlush(users.get(0));
            //userDao.deleteAll();
        }
        System.out.println("A22-mysql" + System.currentTimeMillis());
    }

}
