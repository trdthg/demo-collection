package com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO;

import com.moflowerlkh.decisionengine.domain.entities.User;
import lombok.Data;

import java.util.List;
import java.util.stream.Collectors;

@Data
public
class JoinLoanActivityUserResponseDTO {
    private String username;
    private Long user_id;
    private String user_name;
    private String user_gender;
    private String user_IDnumber;
    private String user_nation;
    private Integer user_age;
    private Long user_overdual;
    private String user_employment;
    private Boolean user_dishonest;

    public static JoinLoanActivityUserResponseDTO fromUser(User user) {
        JoinLoanActivityUserResponseDTO response = new JoinLoanActivityUserResponseDTO();
        response.setUsername(user.getUsername());
        response.setUser_id(user.getId());
        response.setUser_name(user.getName());
        response.setUser_gender(user.getGender().name());
        response.setUser_IDnumber(user.getIDNumber());
        response.setUser_nation(user.getCountry());
        response.setUser_age(user.getAge());
        response.setUser_overdual(user.getOverDual());
        response.setUser_employment(user.getEmployment().name());
        response.setUser_dishonest(user.getDishonest());
        return response;
    }

    public static List<JoinLoanActivityUserResponseDTO> fromUser(List<User> users) {
        return users.stream().map(JoinLoanActivityUserResponseDTO::fromUser).collect(Collectors.toList());
    }
}
