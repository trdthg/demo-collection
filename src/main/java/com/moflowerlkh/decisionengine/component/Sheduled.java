package com.moflowerlkh.decisionengine.component;

import com.moflowerlkh.decisionengine.dao.LoanActivityDao;
import com.moflowerlkh.decisionengine.dao.LoanRuleDao;
import com.moflowerlkh.decisionengine.dao.ShoppingGoodsDao;
import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.LoanActivity;
import com.moflowerlkh.decisionengine.entity.LoanRule;
import com.moflowerlkh.decisionengine.entity.ShoppingGoods;
import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.enums.Employment;
import com.moflowerlkh.decisionengine.enums.Gender;
import com.moflowerlkh.decisionengine.util.RedisUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

@Component
public class Sheduled {

    @Resource
    private RedisUtil redisUtil;

    @Autowired
    UserDao userDao;
    @Autowired
    ShoppingGoodsDao shoppingGoodsDao;
    @Autowired
    LoanActivityDao loanActivityDao;
    @Autowired
    LoanRuleDao loanRuleDao;

    //@Scheduled(cron = "0/30 * * * * ?") //每天开始15秒执行一次
    //public void testRedis(){
    //    String s = String.valueOf(redisUtil.get("a"));
    //    System.out.println(s);
    //    redisUtil.set("a", String.valueOf(System.currentTimeMillis()));
    //
    //    System.out.println("A22-redis" + System.currentTimeMillis());
    //}

    //@Scheduled(cron = "0/30 * * * * ?") //每天开始15秒执行一次
    @PostConstruct
    public void testMysql() {
        List<User> users = userDao.findAll();
        System.out.println(users);
        if (users.isEmpty()) {
            User newUser = new User();
            newUser.setUsername("admin");

            String encodedPassword = new BCryptPasswordEncoder().encode("000000");
            newUser.setPassword(encodedPassword);

            newUser.setYearIncome(10L);
            newUser.setGender(Gender.Male);
            newUser.setEmployment(Employment.Employed);
            newUser.setAge(18);
            newUser.setName("小明");
            newUser.setDishonest(false);
            newUser.setCountry("中国");
            userDao.save(newUser);
            System.out.println("user初始化成功");

            ShoppingGoods shoppingGoods1 = new ShoppingGoods();
            shoppingGoods1.setName("商品1");
            shoppingGoods1.setInfo("商品1的信息");
            shoppingGoods1.setGoodsTotal(1000000L);
            shoppingGoodsDao.save(shoppingGoods1);
            System.out.println("shoppinggoods初始化成功");

            LoanRule loanRule = new LoanRule();
            loanRule.setCheckGuarantee(true);
            loanRule.setMaxAge(65);
            loanRule.setMinAge(18);
            loanRule.setCheckEmployment(true);
            loanRule.setCheckDishonest(true);
            loanRule.setCheckOverDual(true);
            loanRule.setCheckCountry(true);
            //loanRuleDao.save(loanRule);

            LoanActivity loanActivity = new LoanActivity();
            loanActivity.setName("活动1");
            loanActivity.setMaxMoneyLimit(10000);
            loanActivity.setTimeLimit("3/6");
            loanActivity.setReplayLimit("3");
            loanActivity.setApr(4.00);
            loanActivity.setBeginTime(Timestamp.valueOf("2022-1-5 09:20:00"));
            loanActivity.setEndTime(Timestamp.valueOf("2022-1-9 18:00:00"));
            loanActivity.setAmount(10000);
            loanActivity.setRule(loanRule);
            loanActivityDao.save(loanActivity);
            System.out.println("activity和rule初始化成功");
        }
    }

}
