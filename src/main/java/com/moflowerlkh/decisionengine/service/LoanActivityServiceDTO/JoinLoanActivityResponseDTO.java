//package com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO;
//
//import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
//
//import lombok.Data;
//
//import java.util.ArrayList;
//import java.util.List;
//import java.util.stream.Collectors;
//
//@Data
//public class JoinLoanActivityResponseDTO {
//    private List<JoinLoanActivityUserResponseDTO> passed_users;
//    private List<JoinLoanActivityUserResponseDTO> unPassed_users;
//
//    public static JoinLoanActivityResponseDTO fromLoanActivity(LoanActivity loanActivity) {
//        JoinLoanActivityResponseDTO response = new JoinLoanActivityResponseDTO();
//        response.setPassed_users(
//            JoinLoanActivityUserResponseDTO.fromUser(new ArrayList<>(loanActivity.getUserLoanActivities().stream()
//                .filter(x -> x.getIsPassed())
//                .map(x -> x.getUser())
//                .collect(Collectors.toList()))));
//        response.setUnPassed_users(
//            JoinLoanActivityUserResponseDTO.fromUser(new ArrayList<>(loanActivity.getUserLoanActivities().stream()
//                .filter(x -> !x.getIsPassed())
//                .map(x -> x.getUser())
//                .collect(Collectors.toList()))));
//        return response;
//    }
//}
