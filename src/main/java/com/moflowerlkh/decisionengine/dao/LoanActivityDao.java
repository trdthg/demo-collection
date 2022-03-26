package com.moflowerlkh.decisionengine.dao;

import com.moflowerlkh.decisionengine.entity.LoanActivity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LoanActivityDao extends JpaRepository<LoanActivity, Long> {
}
