package com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO;

import com.moflowerlkh.decisionengine.domain.entities.Goods;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.vo.enums.DateValue;
import lombok.Data;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;
import java.sql.Timestamp;

@Data
public
class SetLoanActivityRequest {
    // activity_id string 活动序号
    // activity_name string 活动名称
    @NotEmpty(message = "活动名称不能为空")
    private String activity_name;
    // activity_moneyLimit number 借款额度
    @NotNull(message = "借款额度不能为空")
    @PositiveOrZero(message = "借款额度不能为负")
    private Long activity_moneyLimit;

    // 分几期
    @NotEmpty(message = "借款期限不能为空")
    private String activity_timeLimit;

    // 还几年
    @NotNull(message = "还款期限不能为空")
    @PositiveOrZero(message = "还款期限不能为负")
    private Integer activity_replayTime;

    // 活动开始时间
    @DateValue(message = "活动开始时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    private String activity_startTime;
    // 活动结束时间
    @DateValue(message = "活动结束时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    private String activity_endTime;

    @NotNull(message = "年利率不能为空")
    @PositiveOrZero(message = "年利率不能为负数")
    private double activity_apr;

    @NotNull(message = "产品总数量不能为空")
    @PositiveOrZero(message = "产品总数量必须为0或正整数")
    private Long activity_totalQuantity;
    @NotNull(message = "产品总金额不能为空")
    @PositiveOrZero(message = "产品总金额必须为0或正整数")
    private Long activity_totalAmount;
    @NotNull(message = "起贷金额不能为空")
    @PositiveOrZero(message = "起贷金额必须为>=0")
    private double activity_initMoney;

    @NotNull(message = "步长不能为空")
    @PositiveOrZero(message = "步长必须为0或正整数")
    private Integer activity_perPrice;
    @NotNull(message = "限购份数不能为空")
    @PositiveOrZero(message = "限购份数必须为0或正整数")
    private Integer activity_oneMaxAmount;

    // 活动规则
    @Valid
    @NotNull(message = "活动规则不能为空")
    private SetLoanActivityRuleRequest rule;

    // 活动对应的商品
    // @NotNull(message = "活动对应的商品id不能为空")
    // private Long shoppinggoods_id;

    public LoanActivity toLoanActivity() {
        LoanActivity loanActivity = new LoanActivity();
        // 设置基本信息
        loanActivity.setName(activity_name);
        loanActivity.setMaxMoneyLimit(activity_moneyLimit);
        loanActivity.setTimeLimit(activity_timeLimit);
        loanActivity.setReplayLimit(activity_replayTime);
        loanActivity.setEndTime(Timestamp.valueOf(activity_endTime));
        loanActivity.setBeginTime(Timestamp.valueOf(activity_startTime));
        loanActivity.setApr(activity_apr);
        loanActivity.setPerPrice(activity_perPrice);

        Goods shoppingGoods = new Goods();
        shoppingGoods.setOneMaxAmount(activity_oneMaxAmount);
        shoppingGoods.setStartTime(loanActivity.getBeginTime());
        shoppingGoods.setGoodsAmount(activity_totalQuantity);

        //loanActivity.setShoppingGoods(shoppingGoods);
        loanActivity.setMoneyTotal(activity_totalAmount);
        loanActivity.setMinMoneyLimit(activity_initMoney);

        // 添加规则
        LoanRule loanRule = rule.toLoanRule();
        //loanActivity.setRule(loanRule);

        return loanActivity;
    }
}
