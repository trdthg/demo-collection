package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.*;
import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.enums.Employment;
import com.moflowerlkh.decisionengine.vo.po.BaseResult;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.data.domain.Example;
import org.springframework.http.HttpStatus;
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

    @Autowired
    UserLoanActivityDao userLoanActivityDao;

    public List<LoanActivity> getAllActivities() {
        return loanActivityDao.findAll();
    }

    public void setNewActivity(LoanActivity loanActivity, LoanRule loanRule) {
        loanActivity.setRule(loanRule);
        loanActivityDao.save(loanActivity);
    }

    @Timed("检查用户信息访问耗时")
    @Counted("检查用户信息访问频率")
    public BaseResult<Boolean> checkUserInfo(LoanActivity loanActivity, User user) {
        BaseResult<Boolean> baseResult = new BaseResult<>();
        baseResult.setResult(false);
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
    public BaseResponse<Boolean> tryJoin(Long loanActivityId, Long userId) {
        LoanActivity loanActivity = loanActivityDao.findById(loanActivityId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
        UserLoanActivity userLoanActivity = userLoanActivityDao.findByUserAndLoanActivity(user, loanActivity);
        if (userLoanActivity == null) {
            BaseResult<Boolean> baseResult = new LoanService().checkUserInfo(loanActivity, user);
            userLoanActivityDao.saveAndFlush(
                    UserLoanActivity.builder().user(user).loanActivity(loanActivity).isPassed(baseResult.getResult())
                            .build());
            if (baseResult.getResult()) {
                return new BaseResponse<>(HttpStatus.OK, "初筛通过, 参加成功", true);
            } else {
                return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + baseResult.getMessage(), false);
            }
        } else {
            return new BaseResponse<>(HttpStatus.OK, "您已经参加过", userLoanActivity.getIsPassed());
        }
    }
}
