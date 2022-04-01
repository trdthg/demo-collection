package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.entities.UserLoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.enums.Employment;
import com.moflowerlkh.decisionengine.vo.po.BaseResult;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
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
        loanActivity.setLoanRuleId(loanRule.getId());
        loanActivityDao.save(loanActivity);
    }

}
