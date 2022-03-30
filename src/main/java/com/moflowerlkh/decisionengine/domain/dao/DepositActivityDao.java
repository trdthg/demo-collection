package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.activities.DepositActivity;

import org.springframework.data.jpa.repository.JpaRepository;

public interface DepositActivityDao extends JpaRepository<DepositActivity, Long> {
}
