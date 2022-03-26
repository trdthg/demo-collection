package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.*;
import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.vo.enums.Employment;
import com.moflowerlkh.decisionengine.vo.po.BaseResult;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.stereotype.Service;

import io.micrometer.core.annotation.Counted;
import io.micrometer.core.annotation.Timed;

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

    @Timed("检查用户信息访问耗时")
    @Counted("检查用户信息访问频率")
    public BaseResult<Boolean> checkUserInfo(long activityId, long userId) throws Exception {
        BaseResult<Boolean> baseResult = new BaseResult<>();
        baseResult.setResult(false);
        User user = userDao.findById(userId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该用户: id = " + userId));
        LoanActivity loanActivity = loanActivityDao.findById(activityId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动: id = " + activityId));
        LoanRule loanRule = loanActivity.getRule();
        if (loanRule.getMaxAge() != null && user.getAge() >= loanRule.getMaxAge()) {
            baseResult.setMessage("用户年龄不能高于" + loanRule.getMaxAge());
            return baseResult;
        }
        if (loanRule.getMinAge() != null && user.getAge() < loanRule.getMinAge()) {
            baseResult.setMessage("用户年龄不能低于" + loanRule.getMinAge());
            return baseResult;
        }
        if (loanRule.getCheckCountry() && (!Objects.equals(user.getCountry(), "中国"))) {
            baseResult.setMessage("用户必须来自中国");
            return baseResult;
        }
        if (loanRule.getCheckDishonest() && user.getDishonest()) {
            baseResult.setMessage("用户不能是失信人员");
            return baseResult;
        }
        if (loanRule.getCheckEmployment() && user.getEmployment() != Employment.Employed) {
            baseResult.setMessage("用户必须在值");
            return baseResult;
        }
        if (loanRule.getCheckOverDual() && user.getOverDual() != null && user.getOverDual() > 0) {
            baseResult.setMessage("用户的逾期记录不能超过0次");
            return baseResult;
        }
        baseResult.setResult(true);
        return baseResult;
    }

    @Timed("写入数据库耗时")
    @Counted("写入数据库频率")
    public void tryJoin(Long activityId, Long userId, Boolean checkPass) {
        LoanActivity loanActivity = loanActivityDao.findById(activityId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
        if (checkPass) {
            loanActivity.getPassedUser().add(user);
            loanActivity.getUnPassedUser().remove(user);
            user.getPassedLoanActivities().add(loanActivity);
            user.getUnPassedLoanActivities().remove(loanActivity);
        } else {
            loanActivity.getUnPassedUser().add(user);
            loanActivity.getPassedUser().remove(user);
            user.getUnPassedLoanActivities().add(loanActivity);
            user.getPassedLoanActivities().remove(loanActivity);
        }
        loanActivityDao.saveAndFlush(loanActivity);
        userDao.saveAndFlush(user);
    }
}
