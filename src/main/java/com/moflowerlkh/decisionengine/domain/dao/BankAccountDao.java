package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.BankAccount;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BankAccountDao extends JpaRepository<BankAccount, Long> {
    List<BankAccount> findByUserID(Long userId);

    BankAccount findByBankAccountSN(long sn);

}
