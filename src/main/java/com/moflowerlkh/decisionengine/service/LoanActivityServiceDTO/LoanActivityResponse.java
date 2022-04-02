package com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO;

import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Data
public
class LoanActivityResponse {
    private Long activity_id;
    // activity_id string 活动序号
    private String activity_name;
    // activity_name string 活动名称
    private Double activity_moneyLimit;
    // activity_moneyLimit number 借款额度
    private String activity_timeLimit;
    // activity_timeLimit string 借款期限
    private Integer activity_replayTime;
    // activity_replayTime string 还款期限
    private Double activity_apr;
    // activity_apr string 年利率
    private SetLoanActivityRuleRequest rule;
    // activity_dateRate bool 是否当日起息
    // activity_dawa bool 是否随存随取
    // activity_sum number 产品总数量
    // activity_startTime date 产品秒杀开始时间
    // activity_endTime date 产品秒杀结束时间
    private Long activity_totalQuantity;
    private Long activity_totalAmount;
    private double activity_initMoney;
    // activity_sum number 产品总数量
    private String activity_startTime;
    // activity_startTime date 产品秒杀开始时间
    private String activity_endTime;
    // activity_endTime date 产品秒杀结束时间

    private List<JoinLoanActivityUserResponse> passed_users;
    private List<JoinLoanActivityUserResponse> unPassed_users;

    public static LoanActivityResponse fromLoanActivity(LoanActivity loanActivity) {
        LoanActivityResponse response = new LoanActivityResponse();
        response.setActivity_id(loanActivity.getId());
        response.setActivity_name(loanActivity.getName());
        response.setActivity_moneyLimit(loanActivity.getMaxMoneyLimit());
        response.setActivity_timeLimit(loanActivity.getTimeLimit());
        response.setActivity_replayTime(loanActivity.getReplayLimit());
        response.setActivity_apr(loanActivity.getApr());

        //response.setActivity_totalQuantity(loanActivity.getShoppingGoods().getGoodsAmount());
        response.setActivity_totalAmount(loanActivity.getMoneyTotal());
        response.setActivity_initMoney(loanActivity.getMinMoneyLimit());

        String s = loanActivity.getBeginTime().toString();
        response.setActivity_startTime(s.substring(0, s.indexOf('.')));
        s = loanActivity.getEndTime().toString();
        response.setActivity_endTime(s.substring(0, s.indexOf('.')));

        //response.setRule(SetLoanActivityRuleRequest.fromLoanRule(loanActivity.getRule()));
        // return
        // users.stream().map(JoinLoanActivityUserResponse::fromUser).collect(Collectors.toList());

        response.setPassed_users(JoinLoanActivityUserResponse.fromUser(new ArrayList<>(
            loanActivity.getUserLoanActivities().stream()
                .filter(x -> x.getIsPassed())
                .map(x -> x.getUser())
                .collect(Collectors.toList()))));
        response.setUnPassed_users(
            JoinLoanActivityUserResponse.fromUser(new ArrayList<>(
                loanActivity.getUserLoanActivities().stream()
                    .filter(x -> !x.getIsPassed())
                    .map(x -> x.getUser())
                    .collect(Collectors.toList()))));
        return response;
    }
}
