package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.LoanActivity;

import org.springframework.data.jpa.repository.JpaRepository;

public interface LoanActivityDao extends JpaRepository<LoanActivity, Long> {
}
