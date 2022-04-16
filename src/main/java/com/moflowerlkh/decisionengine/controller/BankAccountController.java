package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.domain.dao.BankAccountDao;
import com.moflowerlkh.decisionengine.domain.entities.BankAccount;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BankAccountController {

    @Autowired
    private BankAccountDao bankAccountDao;

    @PostMapping("/bank-account/{sn}")
    public BaseResponse<BankAccount> bankAccountBaseResponse(@PathVariable Long sn) {
        return new BaseResponse<BankAccount>(bankAccountDao.findByBankAccountSN(sn));
    }

}
