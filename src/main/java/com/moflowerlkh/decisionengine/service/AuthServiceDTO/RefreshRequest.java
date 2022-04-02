package com.moflowerlkh.decisionengine.service.AuthServiceDTO;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public
class RefreshRequest {
    private String refreshToken;
}
