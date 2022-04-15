package com.moflowerlkh.decisionengine.service.DepositeActivityDTO;

import lombok.Builder;
import lombok.Data;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@Data
@Builder
public class GetRuleResponseDTO {
    private Integer activity_ageUp;
    private Integer activity_ageFloor;
    private Boolean activity_dateRate;
    private Boolean activity_dawa;
}
