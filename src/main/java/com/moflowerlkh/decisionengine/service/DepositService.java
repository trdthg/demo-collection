package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.DepositActivityDao;
import com.moflowerlkh.decisionengine.dao.DepositRuleDao;
import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.DepositActivity;
import com.moflowerlkh.decisionengine.entity.DepositRule;
import com.moflowerlkh.decisionengine.entity.User;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.stream.Collectors;

public class DepositService {

    @Autowired
    UserDao userDao;

    @Autowired
    DepositActivityDao depositActivityDao;

    @Autowired
    DepositRuleDao depositRuleDao;

    public List<DepositActivity> getAllActivities() {
        return depositActivityDao.findAll();
    }

    public List<User> getAllPassedUser(long eventID) {
        DepositActivity depositActivity = depositActivityDao.getById(eventID);
        DepositRule depositRule = depositActivity.getRule();
        List<User> users = userDao.findAll();
        return users.stream().filter(x -> {
            if (depositRule.isCheckMaxAge() && x.getAge() > depositRule.getMaxAge()) return false;
            if (depositRule.isCheckMinAge() && x.getAge() < depositRule.getMinAge()) return false;
            if (depositRule.isCheckCountry() && !depositRule.getAllowedCountries().contains(x.getCountry())) return false;
            return true;
        }).collect(Collectors.toList());
    }

}
