package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.*;
import com.moflowerlkh.decisionengine.entity.*;
import com.moflowerlkh.decisionengine.enums.Employment;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Objects;

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

    public boolean checkUserInfo(long activityId, long userId) throws Exception {
        User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户: id = " + userId));
        LoanActivity loanActivity = loanActivityDao.findById(activityId).orElseThrow(() -> new DataRetrievalFailureException("没有该活动: id = " + activityId));
        LoanRule loanRule = loanActivity.getRule();
        System.out.println(loanActivity);
        System.out.println(user);
        if (loanRule.getMaxAge() != null && user.getAge() >= loanRule.getMaxAge()) throw new Exception("用户年龄不能高于" + loanRule.getMaxAge());
        if (loanRule.getMinAge() != null && user.getAge() <= loanRule.getMinAge()) throw new Exception("用户年龄不能低于" + loanRule.getMinAge());
        if (loanRule.getCheckCountry() && (!Objects.equals(user.getCountry(), "中国"))) throw new Exception("用户必须来自中国");
        if (loanRule.getCheckDishonest() && user.getDishonest()) throw new Exception("用户不能是失信人员");
        if (loanRule.getCheckEmployment() && user.getEmployment() != Employment.Employed) throw new Exception("用户必须在值");
        if (loanRule.getCheckOverDual() && user.getOverDual() != null && user.getOverDual() > 0) throw new Exception("用户的逾期记录不能超过0次");
        return true;
    }

    public void tryJoin(long activityId, long userId) {
        LoanActivity loanActivity = loanActivityDao.findById(activityId).orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
        loanActivity.getUsers().add(user);
        user.getLoanActivities().add(loanActivity);
        loanActivityDao.saveAndFlush(loanActivity);
        userDao.saveAndFlush(user);
    }
}
