package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.*;
import com.moflowerlkh.decisionengine.entity.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class LoanService {
    @Autowired
    UserDao userDao;

    @Autowired
    LoanActivityDao loanActivityDao;

    @Autowired
    LoanRuleDao loanRuleDao;

    public List<LoanActivity> getAllActivities() {
        return loanActivityDao.findAll();
    }

    public void setNewActivity(LoanActivity loanActivity, LoanRule loanRule) {
        loanActivity.setRule(loanRule);
        loanActivityDao.save(loanActivity);
    }

    public List<User> getAllPassedUser(long eventID) {
        LoanActivity loanActivity = loanActivityDao.getById(eventID);
        LoanRule loanRule = loanActivity.getRule();
        List<User> users = userDao.findAll();
        return users.stream().filter(x -> {
            //if ( x.getAge() > loanRule.getMaxAge()) return false;
            //if (loanRule.isCheckMinAge() && x.getAge() < loanRule.getMinAge()) return false;
            //if (loanRule.isCheckCountry() && loanRule.getAllowedCountries().contains(x.getCountry())) return false;
            //if (loanRule.isCheckDishonest() && x.isDishonest()) return false;
            //if (loanRule.isCheckEmployment() && !loanRule.getAllowedEmployments().contains(x.getEmployment())) return false;
            return true;
        }).collect(Collectors.toList());
    }
}
