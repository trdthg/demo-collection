package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.dao.LoanActivityDao;
import com.moflowerlkh.decisionengine.entity.LoanActivity;
import com.moflowerlkh.decisionengine.entity.LoanRule;
import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.enums.DateValue;
import com.moflowerlkh.decisionengine.enums.Employment;
import com.moflowerlkh.decisionengine.enums.EnumValue;
import com.moflowerlkh.decisionengine.enums.Gender;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.Data;
import lombok.NonNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.Valid;
import javax.validation.constraints.*;
import java.sql.Timestamp;
import java.util.Date;

@RestController
@Api(tags = {"活动设置相关"})
@RequestMapping("/api/activity")
public class ActivityController {

    @Autowired
    LoanActivityDao loanActivityDao;

    @PostMapping("/set-loan-activity")
    @ApiOperation("新增活动")
    public BaseResponse<Long> setLoanActivity(@RequestBody @Valid SetLoanActivityRequest request) {
        LoanActivity loanActivity = request.toEntity();
        loanActivityDao.save(loanActivity);
        return new BaseResponse<>(HttpStatus.CREATED, "成功", loanActivity.getId());
    }
}

@Data
class SetLoanActivityRuleRequest {
    //activity_guarantee	string	是否需要担保
    @NotNull(message = "是否需要担保不能为空")
    private Boolean activity_guarantee;
    //activity_pledge	string	是否需要抵押
    @NotNull(message = "是否需要抵押不能为空")
    private Boolean activity_pledge;
    //activity_ageUp	number	年龄上限
    @NotNull(message = "年龄上限不能为空")
    @PositiveOrZero(message = "年龄上限必须为0或正整数")
    private Integer activity_ageUp;
    //activity_ageFloor	number	年龄下限
    @PositiveOrZero(message = "年龄下限必须为0或正整数")
    @NotNull(message = "年龄下限不能为空")
    private Integer activity_ageFloor;
    //activity_checkwork	string	是否检查在职
    @NotNull(message = "是否检查在职不能为空")
    private Boolean activity_checkwork;
    //activity_checkDishonest	string	是否检查失信
    @NotNull(message = "是否检查失信人员不能为空")
    private Boolean activity_checkDishonest;
    //activity_checkOverdual	string	是否检查逾期
    @NotNull(message = "是否检查逾期不能为空")
    private Boolean activity_checkOverdual;
    //activity_checkNation	string	是否限制国内
    @NotNull(message = "是否限制国内")
    private Boolean activity_checkNation;

    public LoanRule toLoanRule() {
        LoanRule loanRule = new LoanRule();
        loanRule.setCheckGuarantee(activity_guarantee);
        loanRule.setCheckPledge(activity_pledge);
        loanRule.setMaxAge(activity_ageUp);
        loanRule.setMaxAge(activity_ageFloor);
        loanRule.setCheckEmployment(activity_checkwork);
        loanRule.setCheckDishonest(activity_checkDishonest);
        loanRule.setCheckOverDual(activity_checkOverdual);
        loanRule.setCheckCountry(activity_checkNation);
        return loanRule;
    }
}

@Data
class SetLoanActivityRequest {
    //activity_id	string	活动序号
    //activity_name	string	活动名称
    @NotEmpty(message = "活动名称不能为空")
    private String activity_name;
    //activity_moneyLimit	number	借款额度
    @NotNull(message = "借款额度不能为空")
    @PositiveOrZero
    private Long activity_moneyLimit;

    // 分几期
    @NotEmpty(message = "借款期限不能为空")
    private String activity_timeLimit;

    // 还几年
    @NotEmpty(message = "还款期限不能为空")
    private String activity_replayTime;

    // 活动开始时间
    @DateValue(message = "活动开始时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    private String activity_startTime;
    // 活动结束时间
    @DateValue(message = "活动结束时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    private String activity_endTime;

    @NotNull(message = "年利率不能为空")
    @PositiveOrZero(message = "年利率不能为负数")
    private double activity_apr;
    // 活动规则
    @Valid
    @NotNull(message = "活动规则不能为空")
    private SetLoanActivityRuleRequest ruler;

    public LoanActivity toEntity() {
        LoanActivity loanActivity = new LoanActivity();
        loanActivity.setName(activity_name);
        loanActivity.setMaxMoneyLimit(activity_moneyLimit);
        loanActivity.setTimeLimit(activity_timeLimit);
        loanActivity.setReplayLimit(activity_replayTime);
        loanActivity.setEndTime(Timestamp.valueOf(activity_endTime));
        loanActivity.setBeginTime(Timestamp.valueOf(activity_startTime));
        loanActivity.setApr(activity_apr);

        LoanRule loanRule = ruler.toLoanRule();
        loanRule.setLoanActivity(loanActivity);
        loanActivity.setRule(loanRule);
        return loanActivity;
    }
}


