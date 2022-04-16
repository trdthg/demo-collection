package com.moflowerlkh.decisionengine.service.DepositeActivityDTO;

import com.moflowerlkh.decisionengine.domain.entities.Activity;
import com.moflowerlkh.decisionengine.domain.entities.Goods;
import com.moflowerlkh.decisionengine.domain.entities.rules.DepositRule;
import com.moflowerlkh.decisionengine.vo.enums.DateValue;
import lombok.Builder;
import lombok.Data;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@Data
@Builder
public class GetActivityResponseDTO {

    Long activity_id;

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

    @NotNull(message = "产品总数不能为空")
    @PositiveOrZero(message = "产品总数必须为0或正整数")
    Long activity_totalQuantity;

    @NotNull(message = "产品总数不能为空")
    @PositiveOrZero(message = "产品总数必须为0或正整数")
    Long activity_totalAmount;

    @NotNull(message = "最高份数不能为空")
    @PositiveOrZero(message = "最低份数必须为0或正整数")
    Long activity_oneMaxAmount;

    Long activity_moneyLimit;

    @Valid
    @NotNull(message = "活动规则不能为空")
    GetRuleResponseDTO rule;

    public static GetActivityResponseDTO from(Activity activity, DepositRule rule, Goods goods) {
        GetRuleResponseDTO ruleResponseDTO = GetRuleResponseDTO.builder().activity_ageUp(rule.getMaxAge()).activity_ageFloor(rule.getMinAge()).activity_dawa(rule.getIdDawa()).activity_dateRate(rule.getIsOnDay()).build();

        String startTime = activity.getBeginTime().toString();
        String endTime = activity.getEndTime().toString();
        GetActivityResponseDTO res = GetActivityResponseDTO.builder()
            .rule(ruleResponseDTO)

            .activity_id(activity.getId())
            .activity_apr(rule.getApr())
            .activity_name(activity.getName())
            .activity_timeLimit(rule.getTimeLimit())
            .activity_startTime(startTime.substring(0, startTime.indexOf('.')))
            .activity_endTime(endTime.substring(0, endTime.indexOf(".")))

            .activity_perPrice(goods.getPrice())
            .activity_totalQuantity(rule.getPurchasersNumberLimit())
            .activity_moneyLimit(goods.getGoodsAmount())
            .activity_oneMaxAmount(goods.getOneMaxAmount())
            .activity_totalAmount(rule.getPurchasersNumberLimit() * goods.getPrice() * goods.getOneMaxAmount())
            .build();
        return res;
    }
}
