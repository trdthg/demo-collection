package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.entities.UserLoanActivity;

import org.springframework.data.jpa.repository.JpaRepository;

public interface UserLoanActivityDao extends JpaRepository<UserLoanActivity, Long> {
    UserLoanActivity findByUser(User user);

    UserLoanActivity findByLoanActivity(LoanActivity loanActivity);

    UserLoanActivity findByUserAndLoanActivity(User user, LoanActivity loanActivity);
}
