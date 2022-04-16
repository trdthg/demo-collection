package com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO;

import com.moflowerlkh.decisionengine.domain.entities.Activity;
import com.moflowerlkh.decisionengine.domain.entities.Goods;

import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import lombok.Data;

import java.util.List;

@Data
public
class LoanActivityResponseDTO {
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
    // activity_dateRate bool 是否当日起息
    // activity_dawa bool 是否随存随取
    // activity_sum number 产品总数量
    // activity_startTime date 产品秒杀开始时间
    // activity_endTime date 产品秒杀结束时间
    private Long activity_totalQuantity;
    private Long activity_totalAmount;
    private Long activity_initMoney;
    // activity_sum number 产品总数量
    private String activity_startTime;
    // activity_startTime date 产品秒杀开始时间
    private String activity_endTime;
    // activity_endTime date 产品秒杀结束时间

    //private List<JoinLoanActivityUserResponseDTO> passed_users;
    //private List<JoinLoanActivityUserResponseDTO> unPassed_users;

    private Long activity_oneMaxAmount;
    private Long activity_perPrice;

    public static LoanActivityResponseDTO fromLoanActivity(Activity loanActivity, LoanRule rule, Goods goods) {
        LoanActivityResponseDTO response = new LoanActivityResponseDTO();
        response.setActivity_id(loanActivity.getId());
        response.setActivity_name(loanActivity.getName());

        response.setActivity_timeLimit(rule.getTimeLimit());
        response.setActivity_replayTime(rule.getReplayLimit());
        response.setActivity_apr(rule.getApr());

        response.setActivity_totalQuantity(rule.getPurchasersNumberLimit());
        response.setActivity_totalAmount(goods.getGoodsAmount());
        response.setActivity_oneMaxAmount(goods.getOneMaxAmount());
        response.setActivity_perPrice(goods.getPrice());

        response.setActivity_initMoney(rule.getMinMoneyLimit());
        response.setActivity_moneyLimit(rule.getMaxMoneyLimit());

        String s = loanActivity.getBeginTime().toString();
        response.setActivity_startTime(s.substring(0, s.indexOf('.')));
        s = loanActivity.getEndTime().toString();
        response.setActivity_endTime(s.substring(0, s.indexOf('.')));

        return response;
    }
}
