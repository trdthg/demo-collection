package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.domain.dao.BankAccountDao;
import com.moflowerlkh.decisionengine.domain.entities.BankAccount;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@Api(tags = {"账户管理"})
@RestController
public class BankAccountController {

    @Autowired
    private BankAccountDao bankAccountDao;

    @PostMapping("/bank-account/{userId}")
    @ApiOperation(value = "查询账户信息", notes = "")
    public BaseResponse<List<BankAccount>> bankAccountBaseResponse(@PathVariable Long userId) {
        return new BaseResponse<>(bankAccountDao.findByUserID(userId));
    }

}
