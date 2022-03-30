package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.rules.DepositRule;

import org.springframework.data.jpa.repository.JpaRepository;

public interface DepositRuleDao extends JpaRepository<DepositRule, Long> {
}
