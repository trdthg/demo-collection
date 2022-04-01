package com.moflowerlkh.decisionengine.service.dto;

import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Data
public class JoinLoanActivityResponse {
    private List<JoinLoanActivityUserResponse> passed_users;
    private List<JoinLoanActivityUserResponse> unPassed_users;

    public static JoinLoanActivityResponse fromLoanActivity(LoanActivity loanActivity) {
        JoinLoanActivityResponse response = new JoinLoanActivityResponse();
        response.setPassed_users(
            JoinLoanActivityUserResponse.fromUser(new ArrayList<>(loanActivity.getUserLoanActivities().stream()
                .filter(x -> x.getIsPassed())
                .map(x -> x.getUser())
                .collect(Collectors.toList()))));
        response.setUnPassed_users(
            JoinLoanActivityUserResponse.fromUser(new ArrayList<>(loanActivity.getUserLoanActivities().stream()
                .filter(x -> !x.getIsPassed())
                .map(x -> x.getUser())
                .collect(Collectors.toList()))));
        return response;
    }
}
