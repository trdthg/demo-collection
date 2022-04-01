package com.moflowerlkh.decisionengine.service.dto;

import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import lombok.Data;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@Data
public class SetLoanActivityRuleRequest {
    // activity_guarantee string 是否需要担保
    @NotNull(message = "是否需要担保不能为空")
    private Boolean activity_guarantee;
    // activity_pledge string 是否需要抵押
    @NotNull(message = "是否需要抵押不能为空")
    private Boolean activity_pledge;
    // activity_ageUp number 年龄上限
    @NotNull(message = "年龄上限不能为空")
    @PositiveOrZero(message = "年龄上限必须为0或正整数")
    private Integer activity_ageUp;
    // activity_ageFloor number 年龄下限
    @PositiveOrZero(message = "年龄下限必须为0或正整数")
    @NotNull(message = "年龄下限不能为空")
    private Integer activity_ageFloor;
    // activity_checkwork string 是否检查在职
    @NotNull(message = "是否检查在职不能为空")
    private Boolean activity_checkwork;
    // activity_checkDishonest string 是否检查失信
    @NotNull(message = "是否检查失信人员不能为空")
    private Boolean activity_checkDishonest;
    // activity_checkOverdual string 是否检查逾期
    @NotNull(message = "是否检查逾期不能为空")
    private Boolean activity_checkOverdual;
    // activity_checkNation string 是否限制国内
    @NotNull(message = "是否限制国内")
    private Boolean activity_checkNation;

    public LoanRule toLoanRule() {
        LoanRule loanRule = new LoanRule();
        loanRule.setCheckGuarantee(activity_guarantee);
        loanRule.setCheckPledge(activity_pledge);
        loanRule.setMaxAge(activity_ageUp);
        loanRule.setMinAge(activity_ageFloor);
        loanRule.setCheckEmployment(activity_checkwork);
        loanRule.setCheckDishonest(activity_checkDishonest);
        loanRule.setCheckOverDual(activity_checkOverdual);
        loanRule.setCheckCountry(activity_checkNation);
        return loanRule;
    }

    public static SetLoanActivityRuleRequest fromLoanRule(LoanRule loanRule) {
        SetLoanActivityRuleRequest res = new SetLoanActivityRuleRequest();
        res.setActivity_guarantee(loanRule.getCheckGuarantee());
        res.setActivity_pledge(loanRule.getCheckPledge());
        res.setActivity_ageUp(loanRule.getMaxAge());
        res.setActivity_ageFloor(loanRule.getMinAge());
        res.setActivity_checkwork(loanRule.getCheckEmployment());
        res.setActivity_checkDishonest(loanRule.getCheckDishonest());
        res.setActivity_checkOverdual(loanRule.getCheckOverDual());
        res.setActivity_checkNation(loanRule.getCheckCountry());
        return res;
    }
}
