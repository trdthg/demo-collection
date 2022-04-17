package com.moflowerlkh.decisionengine.service.AuthServiceDTO;

import com.moflowerlkh.decisionengine.vo.enums.Gender;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
public
class JwtResponse {
    private String token;
    private String refreshToken;
    private Long user_id;
    private List<String> account_sn;
    private String username;
    private Gender gender;
}
