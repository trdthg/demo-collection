package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.entities.UserDepositActivity;
import com.moflowerlkh.decisionengine.domain.entities.UserLoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface UserDepositActivityDao extends JpaRepository<UserDepositActivity, Long> {
    UserLoanActivity findByUserId(Long userId);

    UserLoanActivity findByActivityId(Long activityId);

    List<UserLoanActivity> findByUserIdAndActivityId(Long userId, Long activityId);
}
