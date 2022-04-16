package com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO;

import com.moflowerlkh.decisionengine.domain.entities.Activity;
import com.moflowerlkh.decisionengine.domain.entities.Goods;

import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import lombok.Data;

@Data
public
class LoanActivitySimpleResponseDTO {
    private Long activity_id;
    // activity_id string 活动序号
    private String activity_name;
    // activity_name string 活动名称
    private Long activity_moneyLimit;
    // activity_moneyLimit number 借款额度
    private String activity_timeLimit;
    // activity_timeLimit string 借款期限
    private Integer activity_replayTime;
    // activity_replayTime string 还款期限
    private Double activity_apr;
    // activity_apr string 年利率
    private SetLoanActivityRuleRequestDTO rule;
    private Long activity_totalQuantity;
    private Long activity_totalAmount;
    private Long activity_initMoney;
    // activity_sum number 产品总数量
    private String activity_startTime;
    // activity_startTime date 产品秒杀开始时间
    private String activity_endTime;
    // activity_endTime date 产品秒杀结束时间

    private Long activity_oneMaxAmount;
    private Long activity_perPrice;

    public static LoanActivitySimpleResponseDTO fromLoanActivity(Activity loanActivity, LoanRule rule, Goods goods) {
        LoanActivitySimpleResponseDTO response = new LoanActivitySimpleResponseDTO();
        response.setActivity_id(loanActivity.getId());
        response.setActivity_name(loanActivity.getName());
        response.setActivity_timeLimit(rule.getTimeLimit());
        response.setActivity_replayTime(rule.getReplayLimit());
        response.setActivity_apr(rule.getApr());

        response.setActivity_totalQuantity(rule.getPurchasersNumberLimit());
        response.setActivity_totalAmount( -1 * rule.getPurchasersNumberLimit() * goods.getOneMaxAmount() * goods.getPrice());
        response.setActivity_perPrice(goods.getPrice() * -1);
        response.setActivity_oneMaxAmount(goods.getOneMaxAmount());

        response.setActivity_moneyLimit(rule.getMaxMoneyLimit());
        response.setActivity_initMoney(rule.getMinMoneyLimit());

        String s = loanActivity.getBeginTime().toString();
        response.setActivity_startTime(s.substring(0, s.indexOf('.')));
        s = loanActivity.getEndTime().toString();
        response.setActivity_endTime(s.substring(0, s.indexOf('.')));

        //response.setRule(SetLoanActivityRuleRequest.fromLoanRule(loanActivity.getRule()));

        return response;
    }
}
