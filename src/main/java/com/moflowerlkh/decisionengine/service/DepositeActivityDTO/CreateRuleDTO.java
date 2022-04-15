package com.moflowerlkh.decisionengine.service.DepositeActivityDTO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class CreateRuleDTO {

    @NotNull(message = "年龄上限不能为空")
    @PositiveOrZero(message = "年龄上限必须为0或正整数")
    private Integer activity_ageUp;
    // activity_ageFloor number 年龄下限
    @PositiveOrZero(message = "年龄下限必须为0或正整数")
    @NotNull(message = "年龄下限不能为空")
    private Integer activity_ageFloor;

    @NotNull(message = "是否当日起息不能为空")
    private Boolean activity_dateRate;

    @NotNull(message = "是否随存随取不能为空")
    private Boolean activity_dawa;
}
