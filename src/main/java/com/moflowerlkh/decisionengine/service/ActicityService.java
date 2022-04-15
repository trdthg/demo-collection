package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.dao.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.security.authentication.AuthenticationManager;

public class ActicityService {
    @Autowired
    GoodsDao goodsDao;
    @Autowired
    LoanRuleDao loanRuleDao;
    @Autowired
    UserDao userDao;
    @Autowired
    UserActivityDao userActivityDao;
    @Autowired
    RedisService redisService;
    @Autowired
    AuthenticationManager authenticationManager;
    @Autowired
    StringRedisTemplate stringRedisTemplate;
    @Autowired
    BankAccountDao bankAccountDao;
}
