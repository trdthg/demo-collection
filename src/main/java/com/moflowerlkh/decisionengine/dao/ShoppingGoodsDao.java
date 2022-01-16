package com.moflowerlkh.decisionengine.dao;

import com.moflowerlkh.decisionengine.entity.DepositActivity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ShoppingActivityDao extends JpaRepository<DepositActivity, Long> {
}
