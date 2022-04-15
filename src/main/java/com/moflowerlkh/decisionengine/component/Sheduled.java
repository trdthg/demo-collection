package com.moflowerlkh.decisionengine.component;

import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.service.RedisService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;

@Component
public class Sheduled {

    @Resource
    private RedisService redisService;

    @Autowired
    UserDao userDao;
    @Autowired
    GoodsDao shoppingGoodsDao;
    @Autowired
    ActivityDao loanActivityDao;
    @Autowired
    LoanRuleDao loanRuleDao;
    @Autowired
    BankAccountDao bankAccountDao;

    // @Scheduled(cron = "0/30 * * * * ?") //每天开始 15 秒执行一次
    @PostConstruct
    public void testRedis() {
        String s = String.valueOf(redisService.get("a"));
        System.out.println(s);

        System.out.println("A22-redis" + System.currentTimeMillis());
    }

    // @Scheduled(cron = "0/30 * * * * ?") //每天开始 15 秒执行一次
    @PostConstruct
    public void testMysql() {
        //List<User> users = userDao.findAll();
        //System.out.println(users);
        //User newUser = new User();
        //newUser.setId(1L);
        //newUser.setUsername("admin");
        //
        //String encodedPassword = new BCryptPasswordEncoder().encode("000000");
        //newUser.setPassword(encodedPassword);
        //
        //newUser.setYearIncome(10L);
        //newUser.setGender(Gender.Male);
        //newUser.setEmployment(Employment.Employed);
        //newUser.setAge(18);
        //newUser.setName("小明");
        //newUser.setDishonest(false);
        //newUser.setIDNumber("dfsdasfgdfsfgfd");
        //newUser.setCountry("中国");
        //Set<String> roles = new HashSet<>(Arrays.asList("test", "admin"));
        //newUser.setRoles(roles);
        //Hibernate.initialize(newUser.getUserLoanActivities());
        //System.out.println("准备 save User");
        //if (users.isEmpty()) {
        //    userDao.save(newUser);
        //} else {
        //    newUser.setId(users.get(0).getId());
        //}
        //
        //BankAccount bankAccount = new BankAccount();
        //Faker faker = new Faker();
        //bankAccount.setId(1L);
        //bankAccount.setBankAccountSN(faker.random().nextLong());
        //bankAccount.setBalance(1000L);
        //bankAccount.setUserID(newUser.getId());
        //List<BankAccount> accounts = bankAccountDao.findAll();
        //System.out.println("准备 save BankAccount");
        //bankAccountDao.save(bankAccount);
        //bankAccount.setBankAccountSN(faker.random().nextLong());
        //bankAccountDao.save(bankAccount);

        //LoanRule loanRule = new LoanRule();
        //loanRule.setId(1L);
        //loanRule.setCheckGuarantee(true);
        //loanRule.setMaxAge(65);
        //loanRule.setMinAge(18);
        //loanRule.setCheckEmployment(true);
        //loanRule.setCheckDishonest(true);
        //loanRule.setCheckOverDual(true);
        //loanRule.setCheckCountry(true);
        //System.out.println("准备 save 规则");
        //if (loanRuleDao.findAll().isEmpty()) {
        //    loanRuleDao.save(loanRule);
        //}

        //Goods goods = new Goods();
        //goods.setId(1L);
        //goods.setGoodsAmount(10000L);
        //goods.setStartTime(Timestamp.valueOf("2022-1-5 09:20:00"));
        //goods.setOneMaxAmount(1);
        //System.out.println("准备 save 商品");
        //if (loanActivityDao.findAll().isEmpty()) {
        //    shoppingGoodsDao.save(goods);
        //}
        //
        //LoanActivity loanActivity = new LoanActivity();
        //loanActivity.setId(1L);
        //loanActivity.setName("活动 1");
        //loanActivity.setMaxMoneyLimit(10000);
        //loanActivity.setTimeLimit("3/6");
        //loanActivity.setReplayLimit(3);
        //loanActivity.setApr(4.00);
        //loanActivity.setBeginTime(Timestamp.valueOf("2022-1-5 09:20:00"));
        //loanActivity.setEndTime(Timestamp.valueOf("2022-1-9 18:00:00"));
        //
        //loanActivity.setGoodsId(goods.getId());
        //loanActivity.setLoanRuleId(loanRule.getId());
        //
        //System.out.println("准备 save 活动");
        //if (loanActivityDao.findAll().isEmpty()) {
        //    loanActivityDao.save(loanActivity);
        //}
        //System.out.println("activity 和 rule 初始化成功");
    }

}
