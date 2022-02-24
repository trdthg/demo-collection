package com.moflowerlkh.decisionengine.dao;

import com.moflowerlkh.decisionengine.entity.LoanRule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LoanRuleDao extends JpaRepository<LoanRule, Long> {
}
