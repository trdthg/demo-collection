package com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO;

import lombok.Data;

@Data
public class TryJoinResponse {
    Boolean result;
    String md5;
    Long goodId;
    String random;
}
