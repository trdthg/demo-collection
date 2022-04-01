package com.moflowerlkh.decisionengine.component;

import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.domain.entities.Goods;
import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.dao.LoanActivityDao;
import com.moflowerlkh.decisionengine.domain.dao.LoanRuleDao;
import com.moflowerlkh.decisionengine.domain.dao.ShoppingGoodsDao;
import com.moflowerlkh.decisionengine.domain.dao.UserDao;
import com.moflowerlkh.decisionengine.util.RedisUtil;
import com.moflowerlkh.decisionengine.vo.enums.Employment;
import com.moflowerlkh.decisionengine.vo.enums.Gender;

import org.hibernate.Hibernate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import java.sql.Timestamp;
import java.util.*;

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

    // @Scheduled(cron = "0/30 * * * * ?") //每天开始15秒执行一次
    @PostConstruct
    public void testRedis() {
        String s = String.valueOf(redisUtil.get("a"));
        System.out.println(s);
        redisUtil.set("a", String.valueOf(System.currentTimeMillis()));

        System.out.println("A22-redis" + System.currentTimeMillis());
    }

    // @Scheduled(cron = "0/30 * * * * ?") //每天开始15秒执行一次
    @PostConstruct
    public void testMysql() {
        List<User> users = userDao.findAll();
        System.out.println(users);
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
        newUser.setIDNumber("dfsdasfgdfsfgfd");
        newUser.setCountry("中国");

        Set<String> roles = new HashSet<>(Arrays.asList("test", "admin"));
        newUser.setRoles(roles);
        Hibernate.initialize(newUser.getUserLoanActivities());
        System.out.println("准备save User");
        userDao.save(newUser);

        // ShoppingGoods shoppingGoods1 = new ShoppingGoods();
        // shoppingGoods1.setName("商品1");
        // shoppingGoods1.setInfo("商品1的信息");
        // shoppingGoods1.setGoodsAmount(10000L);
        // System.out.println("准备save规则");
        // shoppingGoodsDao.save(shoppingGoods1);

        LoanRule loanRule = new LoanRule();
        loanRule.setCheckGuarantee(true);
        loanRule.setMaxAge(65);
        loanRule.setMinAge(18);
        loanRule.setCheckEmployment(true);
        loanRule.setCheckDishonest(true);
        loanRule.setCheckOverDual(true);
        loanRule.setCheckCountry(true);
        System.out.println("准备save规则");
        // loanRuleDao.save(loanRule);

        LoanActivity loanActivity = new LoanActivity();
        loanActivity.setName("活动1");
        loanActivity.setMaxMoneyLimit(10000);
        loanActivity.setTimeLimit("3/6");
        loanActivity.setReplayLimit(3);
        loanActivity.setApr(4.00);
        loanActivity.setBeginTime(Timestamp.valueOf("2022-1-5 09:20:00"));
        loanActivity.setEndTime(Timestamp.valueOf("2022-1-9 18:00:00"));

        Goods shoppingGoods = new Goods();
        shoppingGoods.setGoodsAmount(10000L);
        shoppingGoods.setStartTime(loanActivity.getBeginTime());
        shoppingGoods.setOneMaxAmount(1);
        System.out.println("准备save商品");
        shoppingGoodsDao.save(shoppingGoods);

        loanActivity.setShoppingGoods(shoppingGoods);
        loanActivity.setRule(loanRule);
        // Hibernate.initialize(loanActivity.getUserLoanActivities());
        loanActivity.setId(154L);
        System.out.println("准备save活动");
        loanActivityDao.save(loanActivity);
        System.out.println("activity和rule初始化成功");
    }

}
