package com.moflowerlkh.decisionengine.service.DepositeActivityDTO;

import com.moflowerlkh.decisionengine.vo.enums.DateValue;
import lombok.*;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;
import java.util.Date;

@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class CreateDepositActivityRequestDTO {

    @NotEmpty(message = "活动名称不能为空")
    String activity_name;

    @NotEmpty(message = "存款期限不能为空")
    String activity_timeLimit;

    @NotNull(message = "年利率不能为空")
    @PositiveOrZero(message = "年利率不能为负数")
    Double activity_apr;


    @DateValue(message = "活动开始时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    String activity_startTime;

    @DateValue(message = "活动结束时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    String activity_endTime;


    @NotNull(message = "步长不能为空")
    @PositiveOrZero(message = "步长必须为0或正整数")
    Long activity_perPrice;

    @NotNull(message = "限制购买总人的数不能为空")
    @PositiveOrZero(message = "限制购买的总人数必须为0或正整数")
    Long activity_totalQuantity;

    @NotNull(message = "最高份数不能为空")
    @PositiveOrZero(message = "最低份数必须为0或正整数")
    Long activity_oneMaxAmount;

    @NotNull(message = "存款总金额不能为空")
    @PositiveOrZero(message = "存款总金额必须为0或正整数")
    Long activity_totalAmount;

    @NotNull(message = "存款额度不能为空")
    @PositiveOrZero(message = "存款额度必须为0或正整数")
    Long activity_moneyLimit;

    @Valid
    @NotNull(message = "活动规则不能为空")
    CreateRuleDTO rule;
}
